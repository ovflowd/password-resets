#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, Date

from db.base import Base

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    token = Column(String)
    claimed = Column(Integer)
    expired = Column(Integer)
    date = Column(Date)

    def __init__(self, username, token, claimed, expired, date):
        self.username = username
        self.token = token
        self.claimed = claimed
        self.expired = expired
        self.date = date