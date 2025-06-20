from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.summary import Summary

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)


    parent_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    parent = relationship("Article", remote_side=[id], backref="children")
    summary = relationship("Summary", back_populates="article", uselist=False)