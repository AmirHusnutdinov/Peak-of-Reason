import sqlalchemy
from .db_session_answers import SqlAlchemyBase


class Answer_db(SqlAlchemyBase):
    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
