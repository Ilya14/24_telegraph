from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36))
    header = db.Column(db.String(100))
    signature = db.Column(db.String(50))
    body = db.Column(db.Text)

    def __init__(self, guid, header, signature, body):
        self.guid = guid
        self.header = header
        self.signature = signature
        self.body = body

    def __repr__(self):
        return '<Article({0}, {1}, {2})>'.format(self.header, self.signature, self.body)
