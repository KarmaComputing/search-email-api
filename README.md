# Check email with python & filter with search criteria


Connect to the specified email account and
print all emails in the Inbox. If set, filter the
emails by search criteria.

Usage api:

https://search-email.dokku.karmacomputing.co.uk/docs # then press 'try it'

Usage command line:
```
    export email_host=email.example.com
    export email_user=bob@example.com
    export email_passord="secret"

    python main.py
```

Usage with search criteria:
```
    export email_host=email.example.com
    export email_user=bob@example.com
    export email_passord="secret"

    export imap_search_subject="Example subject"
    export imap_search_unseen=1 # only show unseen/unread emails
    export imap_search_since_date="22-Jul-2012"

    python main.py
```
