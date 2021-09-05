import imaplib
import os
from email import policy
from email.parser import BytesParser

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

"""
Connect to the specified email account and
print all emails in the Inbox. If set, filter the
emails by search criteria.

Usage:
    export email_host=email.example.com
    export email_user=bob@example.com
    export email_password="secret"

    python main.py

Usage with search criteria:
    export email_host=email.example.com
    export email_user=bob@example.com
    export email_password="secret"

    export imap_search_subject="Example subject"
    export imap_search_unseen=1 # only show unseen/unread emails
    export imap_search_since_date="22-Jul-2012"

    python main.py

"""


email_host = os.getenv("email_host", "email.example.com")
email_user = os.getenv("email_user", "bob@example.com")
email_password = os.getenv("email_password", "secret")

imap_search_subject = os.getenv("imap_search_subject", None)
imap_search_unseen = os.getenv("imap_search_unseen", None)
imap_search_since_date = os.getenv("imap_search_since_date", None)


app = FastAPI()


def search_email(json_output=False):
    # Connect to email server
    imap = imaplib.IMAP4_SSL(os.getenv("email_host"))
    # Login
    imap.login(os.getenv("email_user"), os.getenv("email_password"))
    imap.select("Inbox")

    searchCriteria = ""

    if os.getenv("imap_search_subject"):
        imap_search_subject = os.getenv("imap_search_subject")
        searchCriteria = f'SUBJECT "{imap_search_subject}"'

    if os.getenv("imap_search_unseen"):
        if os.getenv("imap_search_unseen") == "1":
            searchCriteria += " UNSEEN"

    if os.getenv("imap_search_since_date"):
        imap_search_since_date = os.getenv("imap_search_since_date")
        searchCriteria += f" SINCE {imap_search_since_date}"
    if searchCriteria == "":
        # If no search criteria given, fetch all emails
        searchCriteria = "ALL"

    resp, emails = imap.search(None, searchCriteria)
    if json_output:
        json_response = []

    for num in emails[0].split():
        resp, data = imap.fetch(num, "(RFC822)")
        msg = BytesParser(policy=policy.default).parsebytes(data[0][1])
        simplest = msg.get_body(preferencelist=("plain", "html"))
        email_body = "".join(simplest.get_content().splitlines(keepends=True))
        if json_output is False:
            output_seperator = os.getenv("output_seperator", "#" * 80)
            print(email_body)
            print(output_seperator)
        else:
            json_response.append({"email_body": email_body})

    imap.close()
    if json_output:
        return json_response


class EmailSettings(BaseModel):
    email_host: str
    email_user: str
    email_password: str

    imap_search_subject: Optional[str] = None
    imap_search_unseen: Optional[int] = None
    imap_search_since_date: Optional[str] = None


@app.post("/search-email")
async def api_search_email(emailSettings: EmailSettings):
    os.environ["email_host"] = emailSettings.email_host
    os.environ["email_user"] = emailSettings.email_user
    os.environ["email_password"] = emailSettings.email_password

    if emailSettings.imap_search_subject:
        os.environ["imap_search_subject"] = emailSettings.imap_search_subject

    if emailSettings.imap_search_unseen:
        os.environ["imap_search_unseen"] = str(
            emailSettings.imap_search_unseen
        )  # noqa: E501

    if emailSettings.imap_search_since_date:
        os.environ[
            "imap_search_since_date"
        ] = emailSettings.imap_search_since_date  # noqa: E501

    return search_email(json_output=True)
