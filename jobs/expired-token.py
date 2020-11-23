#!/usr/bin/python3

import sys
import os

DOCUMENT_ROOT = os.environ.get('DOCUMENT_ROOT')
sys.path.append(f"{ DOCUMENT_ROOT }/db")

from db.db import Token
from db.base import Session
from datetime import datetime, timedelta

def expired_token():
    tokens = Session.query(Token).all()

    for t in tokens:
        if datetime.now() > t.date + timedelta(hours=1):
            t.expired = 1

    Session.commit()
    Session.close()

expired_token()
