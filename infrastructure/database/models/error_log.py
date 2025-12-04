from sqlalchemy import Column, Integer, String, Text

from infrastructure.database.models.base import BaseModel


class ErrorLogModel(BaseModel):
    __tablename__ = "error_logs"

    error_type = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    traceback = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    client_ip = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
