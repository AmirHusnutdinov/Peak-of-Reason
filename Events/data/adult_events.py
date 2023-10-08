import sqlalchemy
from .db_session_event import SqlAlchemyBase


class Adult_events(SqlAlchemyBase):
    __tablename__ = "adult"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    signature = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    trainings_for_parents = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    individual_consultations = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    the_art_of_communication = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
