from datetime import datetime

from sqlmodel import Field, SQLModel


class Dataset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    filename: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    row_count: int
    rows_dropped: int
    date_min: datetime | None = None
    date_max: datetime | None = None
    total_sales: float


class SalesRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int = Field(foreign_key="dataset.id", index=True)
    order_number: int
    quantity_ordered: int
    price_each: float
    order_line_number: int
    sales: float
    order_date: datetime | None = None
    status: str | None = None
    qtr_id: int | None = None
    month_id: int | None = None
    year_id: int | None = None
    product_line: str | None = None
    msrp: float | None = None
    product_code: str | None = None
    customer_name: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    territory: str | None = None
    deal_size: str | None = None
    total_sales: float
