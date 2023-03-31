import sqlalchemy
from .db_session_event import SqlAlchemyBase


class Event1(SqlAlchemyBase):
    __tablename__ = 'event1'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    photo_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    signature = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
