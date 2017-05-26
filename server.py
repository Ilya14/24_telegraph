from flask import Flask, make_response, redirect, render_template, request, jsonify, abort
from models import db, Article
from werkzeug.contrib.fixers import ProxyFix
from uuid import uuid4

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object('config')
db.init_app(app)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def new_article():
    article_uuid = str(uuid4())
    article = Article(article_uuid, request.form['header'], request.form['signature'], request.form['body'])
    db.session.add(article)
    db.session.commit()
    article_url = '/articles/{0}'.format(article.id)
    response = make_response(redirect(article_url))
    max_cookie_age = 60 * 60 * 24 * 365
    response.set_cookie('uuid', article_uuid, path=article_url, max_age=max_cookie_age)
    return response


@app.route('/articles/<id>')
def article(id):
    article = Article.query.filter_by(id=id).first()
    if article is None:
        abort(404)

    article_uuid = request.cookies.get('uuid')
    if article.uuid == article_uuid:
        return render_template('auth_article.html',
                               id=id,
                               header=article.header,
                               signature=article.signature,
                               body=article.body)
    else:
        return render_template('anonymous_article.html',
                               id=id,
                               header=article.header,
                               signature=article.signature,
                               body=article.body)


@app.route('/articles/<id>/edit/', methods=['GET', 'POST'])
def edit(id):
    article = Article.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('edit.html',
                               id=id,
                               header=article.header,
                               signature=article.signature,
                               body=article.body)
    elif request.method == 'POST':
        article.header = request.form['header']
        article.signature = request.form['signature']
        article.body = request.form['body']
        db.session.add(article)
        db.session.commit()
        return redirect('/articles/{0}'.format(article.id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run()
