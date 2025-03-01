from website.models import MasteryScore, Question, QuestionTag, Submission
from website.extensions import db

def get_next_question(user_id):
    """Fetch the next question based on the user's weakest skill."""
    # Find the weakest skill (tag with lowest mastery score)
    weakest_tag = db.session.query(MasteryScore) \
        .filter_by(userID=user_id) \
        .order_by(MasteryScore.score.asc()) \
        .first()

    if weakest_tag:
        # Get an unattempted question for this tag
        question = db.session.query(Question) \
            .join(QuestionTag, QuestionTag.questionID == Question.questionID) \
            .filter(QuestionTag.tagID == weakest_tag.tagID) \
            .outerjoin(Submission, (Submission.questionID == Question.questionID) & (Submission.userID == user_id)) \
            .filter(Submission.submissionID == None) \
            .order_by(Question.difficulty) \
            .first()
    else:
        # Default: Get any question if no mastery score exists yet
        question = db.session.query(Question).order_by(Question.difficulty).first()

    return question
