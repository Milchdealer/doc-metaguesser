# *-* coding: utf-8 *-*
"""
    Contains the relations in the database and wraps them.
"""
import os
import logging
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Binary,
    Column,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

PAGE_SEPARATOR = "=" * 50

Base = declarative_base()


class DocumentStore(Base):
    __tablename__ = "document_store"
    id = Column(Integer, primary_key=True)
    name = Column(String(1024), nullable=False)
    filename = Column(String(1024), nullable=False)
    content = Column(LONGTEXT())
    page_num = Column(Integer())
    checksum = Column(Binary(40))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class MetadataStore(Base):
    __tablename__ = "document_metadata"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("document_store.id"))
    metadata_label = Column(String(1024), nullable=False)
    metadata_value = Column(String(1024))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


def create_relations(engine, checkfirst: bool = True):
    """ Creates all relations needed. """
    logging.info("Creating all relations.")
    Base.metadata.create_all(engine, checkfirst=checkfirst)


def make_connection():
    """ Returns the engine. """
    sqlalchemy_uri = os.getenv("TXT_METAGUESSER__SQL_ALCHEMY__URI")
    if not sqlalchemy_uri:
        # Try with SQL_ALCHEMY__<params>, might be set by k8s or docker-swarm
        sql_credentials = {
            "user": os.getenv("TXT_METAGUESSER__SQL_ALCHEMY__USER", "root"),
            "password": os.getenv("TXT_METAGUESSER__SQL_ALCHEMY__PASSWORD"),
            "host": os.getenv("TXT_METAGUESSER__SQL_ALCHEMY__HOST", "localhost"),
            "port": os.getenv("TXT_METAGUESSER__SQL_ALCHEMY__PORT", "3307"),
            "database": os.getenv(
                "TXT_METAGUESSER__SQL_ALCHEMY__DATABASE", "documents"
            ),
        }
        library = os.getenv("TXT_METAGUESSER__SQL_ALCHEMY__LIBRARY", "mysql+pymysql")
        sqlalchemy_uri = "%s://%s:%s@%s:%s/%s" % (
            library,
            sql_credentials["user"],
            sql_credentials["password"],
            sql_credentials["host"],
            sql_credentials["port"],
            sql_credentials["database"],
        )
        del sql_credentials
    engine = create_engine(sqlalchemy_uri)
    session = Session(bind=engine)

    return engine, session
