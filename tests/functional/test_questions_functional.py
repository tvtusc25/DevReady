"""Functional tests for the questions API endpoints."""
import pytest
from website.models import Question, TestCase, Tag, QuestionTag
from website.extensions import db

@pytest.fixture
def sample_data(client, app):
    """Create a test user and log them in before running tests."""
    from website.models import User, Tag, Question, QuestionTag, TestCase
    from website.extensions import db
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        test_user = User(username="testuser", email="test@example.com", passwordHash=generate_password_hash("password"))
        db.session.add(test_user)
        db.session.commit()

        client.post("/login", data={"username": "testuser", "password": "password"})

        tag1 = Tag(name="arrays")
        tag2 = Tag(name="strings")
        db.session.add_all([tag1, tag2])
        db.session.commit()
        
        q1 = Question(title="Sum Array", description="Find the sum of array elements", difficulty="easy")
        q2 = Question(title="Reverse String", description="Reverse the given string", difficulty="easy")
        db.session.add_all([q1, q2])
        db.session.commit()

        qt1 = QuestionTag(questionID=q1.questionID, tagID=tag1.tagID)
        qt2 = QuestionTag(questionID=q2.questionID, tagID=tag1.tagID)
        qt3 = QuestionTag(questionID=q2.questionID, tagID=tag2.tagID)
        db.session.add_all([qt1, qt2, qt3])

        tc1 = TestCase(questionID=q1.questionID, inputData="[1, 2, 3]", expectedOutput="6", isSample=True)
        tc2 = TestCase(questionID=q1.questionID, inputData="[4, 5, 6]", expectedOutput="15", isSample=False)
        db.session.add_all([tc1, tc2])

        db.session.commit()
        
        yield  

        db.session.query(TestCase).delete()
        db.session.query(QuestionTag).delete()
        db.session.query(Question).delete()
        db.session.query(Tag).delete()
        db.session.query(User).delete()
        db.session.commit()

def test_get_all_questions(client, sample_data):
    """Test getting all questions endpoint."""
    response = client.get("/questions")
    assert response.status_code == 200
    
    data = response.json
    assert len(data) == 2

    assert data[0]["title"] == "Sum Array"
    assert data[0]["description"] == "Find the sum of array elements"
    assert data[0]["difficulty"] == "easy"
    assert data[0]["tags"] == ["arrays"]
    assert len(data[0]["sample_test_cases"]) == 1
    assert data[0]["sample_test_cases"][0]["input"] == "[1, 2, 3]"
    assert data[0]["sample_test_cases"][0]["expected_output"] == "6"

    assert data[1]["title"] == "Reverse String"
    assert data[1]["description"] == "Reverse the given string"
    assert data[1]["tags"] == ["arrays", "strings"]

def test_get_question_by_id(client, sample_data):
    """Test getting a specific question by ID."""
    response = client.get("/questions/1")
    assert response.status_code == 200
    
    data = response.json
    assert data["title"] == "Sum Array"
    assert data["tags"] == ["arrays"]
    assert len(data["sample_test_cases"]) == 1

    response = client.get("/questions/999")
    assert response.status_code == 404
    assert response.json["error"] == "Question not found"

def test_get_questions_by_tag(client, sample_data):
    """Test getting questions filtered by tag."""
    response = client.get("/questions/tags?tag=arrays")
    assert response.status_code == 200
    
    data = response.json
    assert len(data) == 2

    response = client.get("/questions/tags?tag=strings")
    assert response.status_code == 200
    
    data = response.json
    assert len(data) == 1
    assert data[0]["title"] == "Reverse String"

    response = client.get("/questions/tags")
    assert response.status_code == 400
    assert response.json["error"] == "Tag parameter is required"

    response = client.get("/questions/tags?tag=nonexistent")
    assert response.status_code == 200
    assert len(response.json) == 0

def test_get_question_not_found(client, sample_data):
    """Test getting a non-existent question."""
    response = client.get('/questions/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Question not found'

def test_get_questions_by_tag_missing_param(client, sample_data):
    """Test getting questions by tag without providing tag parameter."""
    response = client.get('/questions/tags')
    assert response.status_code == 400
    assert response.json['error'] == 'Tag parameter is required'

def test_get_questions_by_nonexistent_tag(client, sample_data):
    """Test getting questions with a tag that doesn't exist."""
    response = client.get('/questions/tags?tag=nonexistent')
    assert response.status_code == 200
    assert response.json == []

def test_get_all_questions_empty_db(client, app, sample_data):
    """Test getting questions when database is empty."""
    with app.app_context():
        from website.models import Question, TestCase, QuestionTag
        from website.extensions import db
        
        db.session.query(TestCase).delete()
        db.session.query(QuestionTag).delete()
        db.session.query(Question).delete()
        db.session.commit()
        
        response = client.get("/questions")
        assert response.status_code == 200
        assert response.json == []

def test_get_all_questions_db_error(client, sample_data, mocker):
    """Test database error handling when getting all questions."""
    mock = mocker.patch('website.models.Question.query', 
                       new_callable=mocker.PropertyMock)
    mock.return_value.all.side_effect = Exception("Database error")
    
    response = client.get("/questions")
    assert response.status_code == 500
    assert "error" in response.json
    assert "Failed to fetch questions" in response.json["error"]

def test_get_question_by_id_db_error(client, sample_data, mocker):
    """Test database error handling when getting question by ID."""
    mock = mocker.patch('website.models.Question.query', 
                       new_callable=mocker.PropertyMock)
    mock.return_value.get.side_effect = Exception("Database error")
    
    response = client.get("/questions/1")
    assert response.status_code == 500
    assert "error" in response.json
    assert "Failed to fetch question" in response.json["error"]

def test_get_questions_by_tag_db_error(client, sample_data, mocker):
    """Test database error handling when getting questions by tag."""
    mock_query = mocker.MagicMock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.side_effect = Exception("Database error")
    
    mocker.patch('website.questions.Question.query', mock_query)
    
    response = client.get("/questions/tags?tag=arrays")
    assert response.status_code == 500
    assert "error" in response.json
    assert "Failed to fetch questions by tag" in response.json["error"]

def test_get_questions_by_tag_empty_result(client, sample_data):
    """Test getting questions by tag with no matching results."""
    response = client.get("/questions/tags?tag=nonexistent")
    assert response.status_code == 200
    assert response.json == []

def test_get_questions_malformed_json(client, sample_data, mocker):
    """Test handling of malformed JSON in question data."""
    mocker.patch('website.models.Question.to_dict',
                side_effect=Exception("JSON error"))
    response = client.get("/questions")
    assert response.status_code == 500
    assert "error" in response.json