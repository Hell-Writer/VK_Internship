# VK_Internship

# Description

VKInt is a task for VK Internship summer 2023.

Each user can send, accept or decline friend requests, watch their friend list and check friendship statuses.

Build with Django Rest Framework.

Authorisation implemented with Django auth tokens.

Documented by OpenAPI 3.0.1.

# Intallation:

## - Clone repository

## - Create, and activate virtual enviroment (win)

python -m venv venv

source venv/scripts/activate

## - Install requirements
python -m pip install --upgrade pip

pip install -r requirements.txt

## - Make migrations
python manage.py makemigrations

python manage.py migrate

## - Run server
python manage.py runserver

# API docs could be found in index.html
