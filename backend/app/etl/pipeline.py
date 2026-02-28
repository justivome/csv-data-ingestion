from io import BytesIO

import pandas as pd
from sqlmodel import Session

from app.models.dataset import Dataset, SalesRecord

REQUIRED_COLUMNS = [
    "ORDERNUMBER",
    "QUANTITYORDERED",
    "PRICEEACH",
    "ORDERLINENUMBER",
    "SALES",
    "ORDERDATE",
    "STATUS",
    "QTR_ID",
    "MONTH_ID",
    "YEAR_ID",
    "PRODUCTLINE",
    "MSRP",
    "PRODUCTCODE",
    "CUSTOMERNAME",
    "CITY",
    "COUNTRY",
    "DEALSIZE",
]

NUMERIC_COLUMNS = ["QUANTITYORDERED", "PRICEEACH", "SALES", "MSRP"]


def process_csv(
    file_bytes: bytes, user_id: int, filename: str, session: Session
) -> dict:
    # --- Extract ---
    df = pd.read_csv(BytesIO(file_bytes), encoding="latin-1")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    initial_count = len(df)

    # --- Transform ---
    # Drop rows where key columns are null
    df = df.dropna(subset=["ORDERNUMBER", "PRODUCTCODE"])

    # Deduplicate by ORDERNUMBER + PRODUCTCODE (keep first)
    df = df.drop_duplicates(subset=["ORDERNUMBER", "PRODUCTCODE"], keep="first")

    # Fill numeric nulls with median
    for col in NUMERIC_COLUMNS:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)

    # Parse ORDERDATE
    df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], format="%m/%d/%Y %H:%M", errors="coerce")
    df = df.dropna(subset=["ORDERDATE"])

    # Compute TOTAL_SALES
    df["TOTAL_SALES"] = df["QUANTITYORDERED"] * df["PRICEEACH"]

    rows_dropped = initial_count - len(df)

    # --- Load ---
    date_min = df["ORDERDATE"].min().to_pydatetime()
    date_max = df["ORDERDATE"].max().to_pydatetime()
    total_sales = float(df["TOTAL_SALES"].sum())

    dataset = Dataset(
        user_id=user_id,
        filename=filename,
        row_count=len(df),
        rows_dropped=rows_dropped,
        date_min=date_min,
        date_max=date_max,
        total_sales=total_sales,
    )
    session.add(dataset)
    session.flush()

    records = []
    for _, row in df.iterrows():
        records.append(
            SalesRecord(
                dataset_id=dataset.id,
                order_number=int(row["ORDERNUMBER"]),
                quantity_ordered=int(row["QUANTITYORDERED"]),
                price_each=float(row["PRICEEACH"]),
                order_line_number=int(row["ORDERLINENUMBER"]),
                sales=float(row["SALES"]),
                order_date=row["ORDERDATE"].to_pydatetime(),
                status=row.get("STATUS"),
                qtr_id=int(row["QTR_ID"]) if pd.notna(row.get("QTR_ID")) else None,
                month_id=int(row["MONTH_ID"]) if pd.notna(row.get("MONTH_ID")) else None,
                year_id=int(row["YEAR_ID"]) if pd.notna(row.get("YEAR_ID")) else None,
                product_line=row.get("PRODUCTLINE"),
                msrp=float(row["MSRP"]),
                product_code=row.get("PRODUCTCODE"),
                customer_name=row.get("CUSTOMERNAME"),
                city=row.get("CITY"),
                state=row.get("STATE") if pd.notna(row.get("STATE")) else None,
                country=row.get("COUNTRY"),
                territory=row.get("TERRITORY") if pd.notna(row.get("TERRITORY")) else None,
                deal_size=row.get("DEALSIZE"),
                total_sales=float(row["TOTAL_SALES"]),
            )
        )

    session.add_all(records)
    session.commit()

    return {
        "dataset_id": dataset.id,
        "row_count": dataset.row_count,
        "rows_dropped": dataset.rows_dropped,
        "date_range": {
            "min": date_min.strftime("%Y-%m-%d"),
            "max": date_max.strftime("%Y-%m-%d"),
        },
        "total_sales": total_sales,
    }
