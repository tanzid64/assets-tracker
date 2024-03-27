# Asset Tracker - Device Management API
A django application that provides api for managing enterprise devices, employees, device logs. I made this for REPLIQ as my Jr. Django Job task.

## Features
- Open Company account. And login through JWT authentiaction.
- CRUD operations for employee, devices and device logs.

## API Documentation
PostMan Documentation Link: https://documenter.getpostman.com/view/32603042/2sA35EZNgU


## Deployment

The first thing to do is to clone the repository:

```bash
  git clone https://github.com/tanzid64/assets-tracker.git
  cd assets-tracker
```
Create a virtual environment to install dependencies in and activate it:

```bash
  python -m venv .venv
  .venv\Scripts\activate
```
Then install the dependencies:

```bash
  pip install -r requirements.txt
```

Apply migrations:

```bash
  python manage.py migrate
```
Create an admin account:

```bash
  python manage.py createsuperuser
```
Run test::

```bash
  python manage.py test
```
Start the django application::

```bash
  python manage.py runserver
```

That's it! You should now be able to see the demo application.
Now read the api documentation and use it.

