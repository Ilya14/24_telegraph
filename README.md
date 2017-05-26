# Telegraph Clone

## About project

This site represents the simple tool for the publication of anonymous
articles and is similar to the site http://telegra.ph/.
Any user can post article on the site and receive for it unique url.

Being available a possibility of editing article. Authorization of the
user is carried out on cookies. Storage life of cookies - 1 year.

The site is available at the [address](https://mytelegraph.herokuapp.com/).

## Database creation 

In case of the first application launch it is required to create the
database, having executed the following code:
```python
from server import app, db
with app.app_context():
    db.create_all()
```

## Start of the site

For local start of the site execute:
```sh
$ python3.5 ./server.py
```
The site will be available on http://127.0.0.1:5000/.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
