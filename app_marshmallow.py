import os
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
basedir = os.path.dirname(os.path.dirname(__file__))

# configration attachment  database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app_marshmallow.sqlite3')

ma = Marshmallow(app)
db = SQLAlchemy(app)


# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()
    # Creating database use
    # 1 flask --app app shell
    # 2 from app import db
    # 3 db.create_all()

# models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime, auto_now_add=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.date_created = datetime.now()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")


# model schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('email', 'password', 'date_created')


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    books = ma.auto_field()
    books = ma.List(ma.HyperlinkRelated("book_detail"))


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author

    books = ma.List(ma.HyperlinkRelated("book_detail"))


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True
    author = ma.Nested(AuthorSchema)
    author = ma.HyperlinkRelated("author_detail")


class BookCustomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author')

    author = ma.Nested(AuthorSchema)

    links = ma.Hyperlinks({
        'self': ma.URLFor('book_detail', values=dict(id='<id>')),
        'collection': ma.URLFor('book_list')
    })

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)


# Custom schema
class UserCustomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'date_created', 'link')
    link = ma.HyperlinkRelated("user_detail")
    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )


user_schema = UserCustomSchema()
users_schema = UserCustomSchema(many=True)
# books_schema = BookSchema(many=True)
books_schema = BookCustomSchema(many=True)
book_schema = BookCustomSchema()
author_schema = AuthorSchema()


@app.route('/api/users/', methods=['Post'])
def users_create():
    email = request.json['email']
    password = request.json['password']
    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


@app.route('/api/users/', methods=['GET'])
def users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))


@app.route('/api/users/<int:id>/', methods=['GET'])
def user_detail(id):
    # user = User.query.get(id)
    user = db.get_or_404(User, id)
    return jsonify(user_schema.dump(user))


@app.route('/api/books/<int:id>/', methods=['GET'])
def book_detail(id):
    book = db.get_or_404(Book, id)
    # books = Book.query.get(id)
    return jsonify(book_schema.dump(book))


@app.route('/api/books/', methods=['GET'])
def book_list():
    books = Book.query.all()
    return jsonify(books_schema.dump(books))


@app.route('/api/author/<int:id>/', methods=['GET'])
def author_detail(id):
    author = db.get_or_404(Author, id)
    # books = Book.query.get(id)
    return jsonify(author_schema.dump(author))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
