# Intro

Building a CRM system focused on invoicing and accounting. Current solutions like Akaunting, or Odoo are in my opinion overcomplicated for smaller companies. 
I hope to offer a service that will be an easy tool, written in a powerful framework that can help to administrate, and do invoicing. 

Currently the app has a login system based on sessions. This might be replaced for token authentication in the future, however I first want to research the security drawbacks of this.
I plan to implement a frontend framework like VueJS that can live as an library within Django, this in order to profit from Django's in-build security features. 
Since I am planning to use a SPA as frontend at some point in the future all crud operations will go through the Django Rest Framework.

Middleware is implemented to create a record when the client has viewed an invoice.

Celery Task worker is implemented to send invoices over email. Celery has the advantage over Django RQ that it supports more database types and operate systems.

Signals are used to create or delete an account for every client that is added to the system. I plan to integrate password less login for clients to view their invoices.


# ERD

![ERD DESIGN CRM](https://gitlab.com/ph00lt0/django-crm/-/raw/master/erd/ERD%20CRM%20v0.2.png)


# Installation instructions

- install the requirements in a virtual environment
- create an env file. 
- run migrations
- create a super user
- start the server
- login to the django admin panel
- create at least 1 currency that will be used as default
