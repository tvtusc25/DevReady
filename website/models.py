from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    submissions = db.relationship('Submission', back_populates='user', lazy=True)
    mastery_scores = db.relationship('MasteryScore', back_populates='user', lazy=True)

    def get_id(self):
        return str(self.userID)


class Question(db.Model):
    questionID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    submissions = db.relationship('Submission', back_populates='question', lazy=True)
    questionTags = db.relationship('QuestionTag', back_populates='question', lazy=True)

    @property
    def tags(self):
        return [qt.tag for qt in self.questionTags]


class Tag(db.Model):
    tagID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    questionTags = db.relationship('QuestionTag', back_populates='tag', lazy=True)
    mastery_scores = db.relationship('MasteryScore', back_populates='tag', lazy=True)

    @property
    def questions(self):
        return [qt.question for qt in self.questionTags]


class QuestionTag(db.Model):
    questionTagID = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'))
    tagID = db.Column(db.Integer, db.ForeignKey('tag.tagID'))

    question = db.relationship('Question', back_populates='questionTags')
    tag = db.relationship('Tag', back_populates='questionTags')


class Submission(db.Model):
    submissionID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False)
    result = db.Column(db.String(50), nullable=False)
    runtime = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='submissions')
    question = db.relationship('Question', back_populates='submissions')


class TestCase(db.Model):
    testCaseID = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False)
    inputData = db.Column(db.Text, nullable=False)
    expectedOutput = db.Column(db.Text, nullable=False)
    isSample = db.Column(db.Boolean, default=False)
    
    question = db.relationship('Question', backref='testCases')


class MasteryScore(db.Model):
    __tablename__ = 'mastery_score'
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
    tagID = db.Column(db.Integer, db.ForeignKey('tag.tagID'), primary_key=True)
    score = db.Column(db.Float, nullable=False, default=0.0)

    user = db.relationship('User', back_populates='mastery_scores')
    tag = db.relationship('Tag', back_populates='mastery_scores')
