import imaplib
import pprint
import datetime
import os

"""
Connect to the specified email account and
print all emails in the Inbox. If set, filter the
emails by search criteria.

Usage:
    export email_host=email.example.com
    export email_user=bob@example.com
    export email_passord="secret"

    python main.py

Usage with search criteria:
    export email_host=email.example.com
    export email_user=bob@example.com
    export email_passord="secret"

    export imap_search_subject="Example subject"
    export imap_search_unseen=1 # only show unseen/unread emails
    export imap_search_since_date="22-Jul-2012"

    python main.py

"""

email_host = os.getenv("email_host", "email.example.com")
email_user = os.getenv("email_user", "bob@example.com")
email_passord = os.getenv("email_password", "secret")

imap_search_subject = os.getenv("imap_search_subject", None)
imap_search_unseen = os.getenv("imap_search_unseen", None)
imap_search_since_date = os.getenv("imap_search_since_date", None)

today = datetime.date.today() - datetime.timedelta(days=1)
since = today.strftime("%d-%b-%Y")

# Connect to email server
imap = imaplib.IMAP4_SSL(email_host)
# Login
imap.login(email_user, email_passord)
imap.select("Inbox")

searchCriteria = ""

if imap_search_subject:
    searchCriteria = f'SUBJECT "{imap_search_subject}"'

if imap_search_unseen:
    searchCriteria += " UNSEEN"

if imap_search_since_date:
    searchCriteria += " SINCE {imap_search_since_date}"

if searchCriteria == "":
    # If no search criteria given, fetch all emails
    searchCriteria = "ALL"


resp, emails = imap.search(None, searchCriteria)
for num in emails[0].split():
    resp, data = imap.fetch(num, "(RFC822)")
    print("Message: {0}\n".format(num))
    pprint.pprint(data[0][1])
    break
imap.close()
