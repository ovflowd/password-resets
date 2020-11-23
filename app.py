#!/usr/bin/python3

import uvicorn

import sys
import os

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

DOCUMENT_ROOT = os.environ.get('DOCUMENT_ROOT')

sys.path.append(f"{ DOCUMENT_ROOT }/sysadmin-bin")
sys.path.append(f"{ DOCUMENT_ROOT }/db")

import gnome_ldap_utils

from db.db import Token
from db.base import Session

DOCUMENT_ROOT = os.environ.get('DOCUMENT_ROOT')

LDAP_GROUP_BASE = os.environ.get('LDAP_GROUP_BASE')
LDAP_HOST = os.environ.get('LDAP_HOST')
LDAP_USER_BASE = os.environ.get('LDAP_USER_BASE')
LDAP_USER = os.environ.get('LDAP_USER')
LDAP_PASSWORD = os.environ.get('LDAP_PASSWORD')
LDAP_CA_PATH = os.environ.get('_LDAP_CA_PATH')

SMTP_RELAY_HOST = os.environ.get('SMTP_RELAY_HOST')

glu = gnome_ldap_utils.Gnome_ldap_utils(LDAP_GROUP_BASE, LDAP_HOST, LDAP_USER_BASE, LDAP_USER, LDAP_PASSWORD, LDAP_CA_PATH)

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{DOCUMENT_ROOT}/static"), name="static")

templates = Jinja2Templates(directory=f"{DOCUMENT_ROOT}/templates")

@app.get("/")
def form_get(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.post("/")
def form_post(request: Request, username: str = Form(...)):
    import secrets
    import datetime

    mail = glu.get_attributes_from_ldap(username, 'mail')
    if mail:
        tokens = Session.query(Token.username, Token.expired, Token.claimed).filter(Token.username==username, Token.expired==0, Token.claimed==0)
        if len(list(tokens)) == 1:
            Session.remove()

            return templates.TemplateResponse('general-form.html', context={'request': request, 'badtoken': True})

        date = datetime.datetime.now()
        token = secrets.token_hex(16)

        _token = Token(username, token, 0, 0, date)
        Session.add(_token)
        Session.commit()
        Session.remove()

        send_email(mail.decode('utf-8'), token)

    return templates.TemplateResponse('general-form.html', context={'request': request, 'submitted': True})

@app.get("/reset/{token}")
def form_reset_get(request: Request, token: str):
    t = Session.query(Token).filter(Token.token==token).first()

    if t:
        if not (t.claimed or t.expired):
            from itertools import chain

            infrateam = chain(glu.get_group_from_ldap('accounts'), glu.get_group_from_ldap('sysadmin'), \
                              glu.get_group_from_ldap('admins'))

            if t.username not in infrateam:
                Session.remove()
                return templates.TemplateResponse('form-reset.html', context={'request': request})

    Session.remove()
    return templates.TemplateResponse('general-form.html', context={'request': request, 'badtoken': True})

@app.post("/reset/{token}")
def form_reset_post(request: Request, token: str, password: str = Form(...)):
    newpassword = {'userPassword': password}

    t = Session.query(Token).filter(Token.token==token).first()
    if t:
        try:
            glu.replace_ldap_password(t.username, newpassword['userPassword'].encode())

            t.claimed = 1
            Session.commit()
            Session.remove()

            return templates.TemplateResponse('general-form.html', context={'request': request, 'passwordsuccess': True})
        except:
            Session.remove()

            return templates.TemplateResponse('general-form.html', context={'request': request, 'passworderror': True})

def send_email(email, token):
    import imghdr
    import smtplib

    from jinja2 import Template

    strFrom = 'GNOME Accounts <noreply@gnome.org>'
    strTo = email

    msgRoot = EmailMessage()
    msgRoot['Subject'] = 'GNOME Account Password reset'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot['Reply-To'] = 'gnome-sysadmin@gnome.org'

    with open(f"{DOCUMENT_ROOT}/templates/password_reset_mail.txt", 'r') as _txt:
        t = Template(_txt.read())
        msgRoot.set_content(t.render(token=f"{ token }"))

    with open(f"{DOCUMENT_ROOT}/templates/password_reset_mail.html", 'r') as _html:
        t = Template(_html.read())
        msgRoot.set_content(t.render(token=f"{ token }"), subtype='html')

    with open(f"{DOCUMENT_ROOT}/static/images/GNOME-LogoHorizontal-white.png", 'rb') as _img1:
        image1 = _img1.read()
        msgRoot.add_related(image1, maintype='image',
                            subtype=imghdr.what(None, image1), cid='<image1>')

    with open(f"{DOCUMENT_ROOT}/static/images/Mail-LockSymbol.png", 'rb') as _img2:
        image2 = _img2.read()
        msgRoot.add_related(image2, maintype='image',
                            subtype=imghdr.what(None, image2), cid='<image2>')

    with smtplib.SMTP(f"{SMTP_RELAY_HOST}", 25) as server:
        server.starttls()
        server.sendmail(
            strFrom, strTo, msgRoot.as_string()
        )

if __name__ == '__main__':
    uvicorn.run(app)
