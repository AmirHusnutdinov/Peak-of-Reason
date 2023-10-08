import sqlalchemy
from .db_session_event import SqlAlchemyBase


class Teen_events(SqlAlchemyBase):
    __tablename__ = "teen"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    signature = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    a_piggy_bank_of_possibilities = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    trainings_for_teenagers = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    oratory = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
