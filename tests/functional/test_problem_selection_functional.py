from flask import url_for
from website.models import User, Question, Tag, MasteryScore, QuestionTag
from website.extensions import db

def test_select_problem_based_on_mastery(client, app):
    """Test if the main page recommends a question based on the user's weakest skill."""
    with app.app_context():
        # Create test user
        user = User(username="testuser", email="test@example.com", passwordHash="hashed")
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as session:
            session['_user_id'] = str(user.userID)  # Flask-Login session

        # Create a tag and a mastery score (weak skill)
        tag = Tag(name="Recursion")
        db.session.add(tag)
        db.session.commit()

        mastery = MasteryScore(userID=user.userID, tagID=tag.tagID, score=1)  # Low mastery
        db.session.add(mastery)
        db.session.commit()

        # Create related questions
        question1 = Question(title="Recursion Problem 1", description="Solve this recursion problem.", difficulty="Easy")
        question2 = Question(title="Recursion Problem 2", description="Another recursion problem.", difficulty="Medium")
        db.session.add_all([question1, question2])
        db.session.commit()

        # Link questions to tag
        db.session.add_all([
            QuestionTag(questionID=question1.questionID, tagID=tag.tagID),
            QuestionTag(questionID=question2.questionID, tagID=tag.tagID)
        ])
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    assert b"Recursion Problem" in response.data

def test_select_any_problem_for_new_user(client, app):
    """Test if the main page recommends any question for a new user without mastery scores."""
    with app.app_context():
        user = User(username="newuser", email="new@example.com", passwordHash="hashed")
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as session:
            session['_user_id'] = str(user.userID)  # Flask-Login session
        
        question1 = Question(title="Intro Question", description="Solve this simple problem.", difficulty="Easy")
        db.session.add(question1)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    assert b"Intro Question" in response.data