import os
from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.dirname(os.path.dirname(__file__))

# configration attachment  database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite3')



# configration attachment
db = SQLAlchemy(app)
ma = Marshmallow(app)



# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()
    # Creating database use 
    # 1 flask --app app shell
    # 2 from app import db
    # 3 db.create_all()


# model as in django
class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(255))

    def __init__(self, title, content):
        self.title = title
        self.content = content

# same as serializer in django
class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@app.route('/note/', methods=['GET'])
def get_note():
    all_notes = NoteModel.query.all()
    return jsonify(notes_schema.dump(all_notes))

@app.route('/note/', methods=['POST'])
def create_note():
    title = request.json.get("title")
    content = request.json.get("content")
    note = NoteModel(title, content)
    db.session.add(note)
    db.session.commit()
    return note_schema.jsonify(note)


# @app.route('/note/<int:note_id>/', methods=['GET'])
# def note_detail(note_id):
#     note = NoteModel.query.get(note_id)
#     return jsonify(note)

# @app.route('/note/<int:note_id>/', methods=['GET'])
# def update_note(note_id):
#     note = NoteModel.query.get(note_id)
#     title = request.json.get("title")
#     content = request.json.get("content")
#     note.title = title
#     note.content = content
#     db.session.add(note)
#     db.session.commit()


@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
