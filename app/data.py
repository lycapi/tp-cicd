import copy

INITIAL_STUDENTS = [
    {
        "id": 1,
        "firstName": "Alice",
        "lastName": "Dupont",
        "email": "alice.dupont@example.com",
        "grade": 16.5,
        "field": "informatique"
    },
    {
        "id": 2,
        "firstName": "Bob",
        "lastName": "Martin",
        "email": "bob.martin@example.com",
        "grade": 14.0,
        "field": "mathématiques"
    },
    {
        "id": 3,
        "firstName": "Charlie",
        "lastName": "Durand",
        "email": "charlie.durand@example.com",
        "grade": 12.0,
        "field": "physique"
    },
    {
        "id": 4,
        "firstName": "Diana",
        "lastName": "Lefebvre",
        "email": "diana.lefebvre@example.com",
        "grade": 18.0,
        "field": "chimie"
    },
    {
        "id": 5,
        "firstName": "Eve",
        "lastName": "Bernard",
        "email": "eve.bernard@example.com",
        "grade": 15.5,
        "field": "informatique"
    },
]

ALLOWED_FIELDS = ["informatique", "mathématiques", "physique", "chimie"]
students_db = []
next_id = 6


def reset_data():
    global next_id
    students_db.clear()
    students_db.extend(copy.deepcopy(INITIAL_STUDENTS))
    next_id = 6


def get_next_id():
    global next_id
    current = next_id
    next_id += 1
    return current


reset_data()
