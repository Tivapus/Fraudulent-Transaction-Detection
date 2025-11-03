import databases
import sqlalchemy

DATABASE_URL = "sqlite:///fraud_cases.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

fraudulent_transactions = sqlalchemy.Table(
    "fraudulent_transactions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("time_ind", sqlalchemy.Integer),
    sqlalchemy.Column("transac_type", sqlalchemy.String),
    sqlalchemy.Column("amount", sqlalchemy.Float),
    sqlalchemy.Column("src_acc", sqlalchemy.String),
    sqlalchemy.Column("dst_acc", sqlalchemy.String),
    sqlalchemy.Column("src_bal", sqlalchemy.Float),
    sqlalchemy.Column("src_new_bal", sqlalchemy.Float),
    sqlalchemy.Column("dst_bal", sqlalchemy.Float),
    sqlalchemy.Column("dst_new_bal", sqlalchemy.Float),
    sqlalchemy.Column("is_flagged_fraud", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)