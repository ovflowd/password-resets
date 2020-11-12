#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

DATABASE = 'mysql+pymysql://%s:%s@%s:%i/%s?charset=utf8' % (
    os.environ.get('DATABASE_USERNAME'),
    os.environ.get('DATABASE_PASSWORD'),
    os.environ.get('DATABASE_HOST'),
    os.environ.get('DATABASE_PORT'),
    os.environ.get('DATABASE_NAME'),
)

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True
)

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
