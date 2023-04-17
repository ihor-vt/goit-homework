from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table


Base = declarative_base()

tag_m2m_quote = Table(
    "tag_m2m_quote", Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("tag", Integer, ForeignKey("tags.id")),
    Column("quote", Integer, ForeignKey("quotes.id")),
)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    href_author = Column(String(120), nullable=False, unique=True)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False, unique=True)


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey(Author.id, ondelete="CASCADE"))
    tags = relationship("Tag", secondary=tag_m2m_quote, backref="quotes")
