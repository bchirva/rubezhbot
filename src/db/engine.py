from sqlalchemy import create_engine

# pylint: disable=unused-import

db_engine = create_engine("sqlite:///db.sqlite3")
