from io import BytesIO

import pandas as pd
from fastapi import APIRouter, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlmodel import col, func, select

from app.deps import CurrentUserDep, SessionDep
from app.etl.pipeline import process_csv
from app.models.dataset import Dataset, SalesRecord
from app.schemas.dataset import (
    AggregatesResponse,
    DatasetDetailResponse,
    DatasetListResponse,
    DatasetRead,
    SalesByMonth,
    SalesRecordRead,
    UploadResponse,
)

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
def upload_csv(file: UploadFile, user: CurrentUserDep, session: SessionDep):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are accepted",
        )

    file_bytes = file.file.read()

    try:
        result = process_csv(file_bytes, user.id, file.filename, session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return result


@router.get("/datasets", response_model=DatasetListResponse)
def list_datasets(user: CurrentUserDep, session: SessionDep):
    datasets = session.exec(
        select(Dataset).where(Dataset.user_id == user.id).order_by(col(Dataset.uploaded_at).desc())
    ).all()
    return DatasetListResponse(datasets=[DatasetRead.model_validate(d) for d in datasets])


@router.get("/datasets/{dataset_id}", response_model=DatasetDetailResponse)
def get_dataset(
    dataset_id: int,
    user: CurrentUserDep,
    session: SessionDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    sort_by: str = Query("id", pattern="^(id|order_number|order_date|sales|total_sales|customer_name|product_line|country|status)$"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    status_filter: str | None = Query(None, alias="status"),
    product_line: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset or dataset.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    # Build query for records
    query = select(SalesRecord).where(SalesRecord.dataset_id == dataset_id)

    if status_filter:
        query = query.where(SalesRecord.status == status_filter)
    if product_line:
        query = query.where(SalesRecord.product_line == product_line)
    if date_from:
        query = query.where(col(SalesRecord.order_date) >= date_from)
    if date_to:
        query = query.where(col(SalesRecord.order_date) <= date_to)

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Sort
    sort_col = getattr(SalesRecord, sort_by)
    if sort_order == "desc":
        query = query.order_by(col(sort_col).desc())
    else:
        query = query.order_by(col(sort_col).asc())

    # Paginate
    offset = (page - 1) * page_size
    records = session.exec(query.offset(offset).limit(page_size)).all()

    # Aggregates (over all records in dataset, not filtered)
    all_records = session.exec(
        select(SalesRecord).where(SalesRecord.dataset_id == dataset_id)
    ).all()

    sales_by_product_line: dict[str, float] = {}
    sales_by_country: dict[str, float] = {}
    sales_by_month_map: dict[str, float] = {}

    for r in all_records:
        if r.product_line:
            sales_by_product_line[r.product_line] = (
                sales_by_product_line.get(r.product_line, 0) + r.total_sales
            )
        if r.country:
            sales_by_country[r.country] = sales_by_country.get(r.country, 0) + r.total_sales
        if r.order_date:
            month_key = r.order_date.strftime("%Y-%m")
            sales_by_month_map[month_key] = sales_by_month_map.get(month_key, 0) + r.total_sales

    sales_by_month = [
        SalesByMonth(month=k, total=v) for k, v in sorted(sales_by_month_map.items())
    ]

    return DatasetDetailResponse(
        dataset=DatasetRead.model_validate(dataset),
        records=[SalesRecordRead.model_validate(r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
        aggregates=AggregatesResponse(
            sales_by_product_line=sales_by_product_line,
            sales_by_country=sales_by_country,
            sales_by_month=sales_by_month,
        ),
    )


@router.get("/datasets/{dataset_id}/export")
def export_dataset(
    dataset_id: int,
    user: CurrentUserDep,
    session: SessionDep,
    format: str = Query("csv", pattern="^(csv|parquet)$"),
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset or dataset.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    records = session.exec(
        select(SalesRecord).where(SalesRecord.dataset_id == dataset_id)
    ).all()

    df = pd.DataFrame([r.model_dump() for r in records])

    buf = BytesIO()
    base_name = dataset.filename.rsplit(".", 1)[0] if "." in dataset.filename else dataset.filename

    if format == "parquet":
        df.to_parquet(buf, index=False)
        buf.seek(0)
        return StreamingResponse(
            buf,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.parquet"'},
        )
    else:
        df.to_csv(buf, index=False)
        buf.seek(0)
        return StreamingResponse(
            buf,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.csv"'},
        )
