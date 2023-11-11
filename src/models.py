from . import db, bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(40), unique=True, nullable=False)
    username = db.Column(db.VARCHAR(40), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    notes = db.relationship('Notes', backref='user', lazy=True)
    
    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password, 12)
        self.role = role
        
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_id(self):
        return str(self.id)
    
class Notes(db.Model):

    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.Text)
    grade = db.Column(db.Integer)
    school_type = db.Column(db.Text)
    chapter = db.Column(db.Text)
    content = db.Column(db.Text, nullable = False)
    private = db.Column(db.Integer)
    has_flashcards = db.Column(db.Boolean, default=False)
    flashcards = db.relationship('Flashcards', backref='note', lazy=True)

    def __init__(self, owner_id, content, subject = '', grade = '', school_type = '', chapter= '', private = '0'):
        self.owner_id = owner_id
        self.subject = subject.lower()
        self.grade = grade
        self.school_type = school_type
        self.chapter = chapter
        self.content = content
        self.private = int(private)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Flashcards(db.Model):

    __tablename__ = "flashcard"

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    box = db.Column(db.Integer)
    front =  db.Column(db.Text, nullable = False)
    back =  db.Column(db.Text, nullable = False)
    last_repetition = db.Column(db.DateTime)
    
    def __init__(self, note_id, front, back, box = 0):
        self.note_id = note_id
        self.front = front
        self.back = back
        self.box = box
