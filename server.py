from flask import Flask, render_template, request, jsonify, abort
from models import db, Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
db.init_app(app)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def new_article():
    guid = request.cookies.get('guid')
    article = Article(guid, request.form['header'], request.form['signature'], request.form['body'])
    db.session.add(article)
    db.session.commit()
    return jsonify({'url': '/articles/{0}'.format(article.id)})


@app.route('/articles/<id>')
def article(id):
    guid = request.cookies.get('guid')
    article = Article.query.filter_by(id=id).first()

    if article is None:
        abort(404)

    if article.guid == guid:
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
        return jsonify({'url': '/articles/{0}'.format(article.id)})


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run()
