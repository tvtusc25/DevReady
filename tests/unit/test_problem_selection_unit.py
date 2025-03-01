from website.models import User, Question, Tag, MasteryScore, QuestionTag
from website.extensions import db
from website.views import get_next_question

def test_get_next_question_with_weak_skill(app):
    """Test that the function selects an unattempted question based on weakest skill."""
    with app.app_context():
        # Create test user
        user = User(username="testuser", email="test@example.com", passwordHash="hashed")
        db.session.add(user)
        db.session.commit()

        # Create a tag and a mastery score (low score = weak skill)
        tag = Tag(name="Recursion")
        db.session.add(tag)
        db.session.commit()

        mastery = MasteryScore(userID=user.userID, tagID=tag.tagID, score=1)
        db.session.add(mastery)
        db.session.commit()

        # Create questions related to the tag
        question1 = Question(title="Recursion Problem 1", description="Solve this recursion problem.", difficulty="Easy")
        question2 = Question(title="Recursion Problem 2", description="Another recursion problem.", difficulty="Medium")
        db.session.add_all([question1, question2])
        db.session.commit()

        # Link questions to tag
        db.session.add_all([
            QuestionTag(questionID=question1.questionID, tagID=tag.tagID),
            QuestionTag(questionID=question2.questionID, tagID=tag.tagID)
        ])

        question = get_next_question(user.userID)
        assert question is not None
        assert question.title.startswith("Recursion Problem")

def test_get_next_question_without_mastery_scores(app):
    """Test that a user without mastery scores gets any available question."""
    with app.app_context():
        user = User(username="newuser", email="new@example.com", passwordHash="hashed")
        db.session.add(user)
        db.session.commit()

        question1 = Question(title="Intro Question", description="Solve this simple problem.", difficulty="Easy")
        db.session.add(question1)
        db.session.commit()

        question = get_next_question(user.userID)
        assert question is not None
