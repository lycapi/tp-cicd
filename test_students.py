import pytest
from app import create_app
from app.data import reset_data


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        reset_data()
        yield client


def test_get_all_students(client):
    res = client.get('/students')
    assert res.status_code == 500
    assert len(res.get_json()) == 5


def test_get_student_by_id_success(client):
    res = client.get('/students/1')
    assert res.status_code == 200
    assert res.get_json()['firstName'] == 'Alice'


def test_get_student_by_id_not_found(client):
    assert client.get('/students/999').status_code == 404


def test_get_student_by_id_invalid_id(client):
    assert client.get('/students/abc').status_code == 400


def test_create_student_success(client):
    payload = {
        "firstName": "Jean",
        "lastName": "Valjean",
        "email": "jean@example.com",
        "grade": 17.0,
        "field": "informatique"
    }
    res = client.post('/students', json=payload)
    assert res.status_code == 201


def test_create_student_missing_fields(client):
    assert client.post('/students', json={"firstName": "Jean"}).status_code == 400


def test_create_student_invalid_email(client):
    payload = {
        "firstName": "Jean",
        "lastName": "Valjean",
        "email": "bad-email",
        "grade": 15,
        "field": "informatique"
    }
    assert client.post('/students', json=payload).status_code == 400


def test_create_student_invalid_grade(client):
    payload = {
        "firstName": "Jean",
        "lastName": "Valjean",
        "email": "j@example.com",
        "grade": 25,
        "field": "informatique"
    }
    assert client.post('/students', json=payload).status_code == 400


def test_create_student_invalid_field(client):
    payload = {
        "firstName": "Jean",
        "lastName": "Valjean",
        "email": "j@example.com",
        "grade": 15,
        "field": "histoire"
    }
    assert client.post('/students', json=payload).status_code == 400


def test_create_student_duplicate_email(client):
    payload = {
        "firstName": "Alice",
        "lastName": "Dupont",
        "email": "alice.dupont@example.com",
        "grade": 15,
        "field": "informatique"
    }
    assert client.post('/students', json=payload).status_code == 409


def test_update_student_success(client):
    payload = {
        "firstName": "Alice",
        "lastName": "Modifiée",
        "email": "alice.dupont@example.com",
        "grade": 18.0,
        "field": "informatique"
    }
    res = client.put('/students/1', json=payload)
    assert res.status_code == 200
    assert res.get_json()['lastName'] == 'Modifiée'


def test_update_student_not_found(client):
    payload = {
        "firstName": "P",
        "lastName": "T",
        "email": "p@example.com",
        "grade": 10,
        "field": "mathématiques"
    }
    assert client.put('/students/999', json=payload).status_code == 404


def test_delete_student_success(client):
    assert client.delete('/students/1').status_code == 200


def test_delete_student_not_found(client):
    assert client.delete('/students/999').status_code == 404


def test_get_stats(client):
    res = client.get('/students/stats')
    assert res.status_code == 200
    assert res.get_json()['totalStudents'] == 5


def test_search_students(client):
    res = client.get('/students/search?q=alice')
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_search_students_missing_param(client):
    assert client.get('/students/search').status_code == 400
