import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.etl.pipeline import process_csv

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


def make_csv(rows: list[str]) -> bytes:
    header = "ORDERNUMBER,QUANTITYORDERED,PRICEEACH,ORDERLINENUMBER,SALES,ORDERDATE,STATUS,QTR_ID,MONTH_ID,YEAR_ID,PRODUCTLINE,MSRP,PRODUCTCODE,CUSTOMERNAME,PHONE,ADDRESSLINE1,ADDRESSLINE2,CITY,STATE,POSTALCODE,COUNTRY,TERRITORY,CONTACTLASTNAME,CONTACTFIRSTNAME,DEALSIZE"
    return ("\n".join([header] + rows)).encode()


SAMPLE_ROW = "10107,30,95.7,2,2871,2/24/2003 0:00,Shipped,1,2,2003,Motorcycles,95,S10_1678,Land of Toys Inc.,2125557818,897 Long Airport Avenue,,NYC,NY,10022,USA,NA,Yu,Kwai,Small"
SAMPLE_ROW_2 = "10121,34,81.35,5,2765.9,5/7/2003 0:00,Shipped,2,5,2003,Motorcycles,95,S10_2222,Reims Collectables,26.47.1555,59 rue de l'Abbaye,,Reims,,51100,France,EMEA,Henriot,Paul,Small"


def test_dedup_by_ordernumber_productcode():
    # Same ORDERNUMBER + PRODUCTCODE = duplicate
    csv_data = make_csv([SAMPLE_ROW, SAMPLE_ROW])
    with Session(engine) as session:
        result = process_csv(csv_data, user_id=1, filename="test.csv", session=session)
    assert result["row_count"] == 1
    assert result["rows_dropped"] == 1


def test_numeric_null_filling():
    # Replace PRICEEACH with empty to test median fill
    row_with_null = "10107,30,,2,2871,2/24/2003 0:00,Shipped,1,2,2003,Motorcycles,95,S10_1678,Land of Toys Inc.,2125557818,897 Long Airport Avenue,,NYC,NY,10022,USA,NA,Yu,Kwai,Small"
    csv_data = make_csv([SAMPLE_ROW_2, row_with_null])
    with Session(engine) as session:
        result = process_csv(csv_data, user_id=1, filename="test.csv", session=session)
    # Should not drop the row - null gets filled with median
    assert result["row_count"] == 2


def test_orderdate_parsing():
    csv_data = make_csv([SAMPLE_ROW])
    with Session(engine) as session:
        result = process_csv(csv_data, user_id=1, filename="test.csv", session=session)
    assert result["date_range"]["min"] == "2003-02-24"
    assert result["date_range"]["max"] == "2003-02-24"


def test_total_sales_calculation():
    csv_data = make_csv([SAMPLE_ROW])
    with Session(engine) as session:
        result = process_csv(csv_data, user_id=1, filename="test.csv", session=session)
    # 30 * 95.7 = 2871.0
    assert result["total_sales"] == 30 * 95.7


def test_missing_columns_raises_error():
    csv_data = b"COL1,COL2\n1,2"
    with Session(engine) as session, pytest.raises(ValueError, match="Missing required columns"):
        process_csv(csv_data, user_id=1, filename="test.csv", session=session)
