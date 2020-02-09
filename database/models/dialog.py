from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class Dialog(db.Model):
    __tablename__ = 'dialogs'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID валюты')
    question = db.Column(db.String(), nullable=False, comment='Вопрос')
    answer = db.Column(db.String(), nullable=False, comment='Ответ')
    vector = db.Column(db.NDArray(), nullable=False, comment='Векторы признаков фото')
