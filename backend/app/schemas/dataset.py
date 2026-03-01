from datetime import datetime

from pydantic import BaseModel


class DatasetRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    filename: str
    uploaded_at: datetime
    row_count: int
    rows_dropped: int
    date_min: datetime | None
    date_max: datetime | None
    total_sales: float


class DatasetListResponse(BaseModel):
    datasets: list[DatasetRead]


class SalesRecordRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    dataset_id: int
    order_number: int
    quantity_ordered: int
    price_each: float
    order_line_number: int
    sales: float
    order_date: datetime | None
    status: str | None
    qtr_id: int | None
    month_id: int | None
    year_id: int | None
    product_line: str | None
    msrp: float | None
    product_code: str | None
    customer_name: str | None
    city: str | None
    state: str | None
    country: str | None
    territory: str | None
    deal_size: str | None
    total_sales: float


class SalesByMonth(BaseModel):
    month: str
    total: float


class AggregatesResponse(BaseModel):
    sales_by_product_line: dict[str, float]
    sales_by_country: dict[str, float]
    sales_by_month: list[SalesByMonth]


class DatasetDetailResponse(BaseModel):
    dataset: DatasetRead
    records: list[SalesRecordRead]
    total: int
    page: int
    page_size: int
    aggregates: AggregatesResponse


class UploadResponse(BaseModel):
    dataset_id: int
    row_count: int
    rows_dropped: int
    date_range: dict[str, str]
    total_sales: float
