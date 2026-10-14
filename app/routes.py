import re
from flask import Blueprint, request, jsonify
from app.data import students_db, get_next_id, ALLOWED_FIELDS

students_bp = Blueprint('students', __name__)
EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


@students_bp.route('/stats', methods=['GET'])
def get_stats():
    total = len(students_db)
    if total == 0:
        return jsonify({
            "totalStudents": 0,
            "averageGrade": 0.0,
            "studentsByField": {f: 0 for f in ALLOWED_FIELDS},
            "bestStudent": None
        }), 200

    sum_grades = sum(s["grade"] for s in students_db)
    average_grade = round(sum_grades / total, 2)
    by_field = {f: len([s for s in students_db if s["field"] == f]) for f in ALLOWED_FIELDS}
    best_student = max(students_db, key=lambda s: s["grade"])

    return jsonify({
        "totalStudents": total,
        "averageGrade": average_grade,
        "studentsByField": by_field,
        "bestStudent": best_student
    }), 200


@students_bp.route('/search', methods=['GET'])
def search_students():
    q = request.args.get('q')
    if not q or not q.strip():
        return jsonify({"error": "Le paramètre 'q' est obligatoire."}), 400

    query = q.strip().lower()
    results = [
        s for s in students_db
        if query in s["firstName"].lower() or query in s["lastName"].lower()
    ]
    return jsonify(results), 200


@students_bp.route('', methods=['GET'])
def get_all_students():
    return jsonify(students_db), 200


@students_bp.route('/<id_param>', methods=['GET'])
def get_student_by_id(id_param):
    try:
        student_id = int(id_param)
    except ValueError:
        return jsonify({"error": "L'ID doit être un nombre."}), 400

    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Étudiant non trouvé."}), 404

    return jsonify(student), 200


@students_bp.route('', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    fn = data.get("firstName")
    ln = data.get("lastName")
    email = data.get("email")
    grade = data.get("grade")
    field = data.get("field")

    if not all([fn, ln, email, field]) or grade is None:
        return jsonify({"error": "Tous les champs sont obligatoires."}), 400

    if len(fn) < 2 or len(ln) < 2:
        return jsonify({"error": "Prénom/Nom trop court."}), 400

    if not re.match(EMAIL_REGEX, str(email)):
        return jsonify({"error": "Email invalide."}), 400

    if not isinstance(grade, (int, float)) or isinstance(grade, bool) or not (0 <= grade <= 20):
        return jsonify({"error": "Note invalide."}), 400

    if field not in ALLOWED_FIELDS:
        return jsonify({"error": "Filière invalide."}), 400

    if any(s["email"] == email for s in students_db):
        return jsonify({"error": "Email déjà utilisé."}), 409

    new_student = {
        "id": get_next_id(),
        "firstName": fn,
        "lastName": ln,
        "email": email,
        "grade": float(grade),
        "field": field
    }
    students_db.append(new_student)
    return jsonify(new_student), 201


@students_bp.route('/<id_param>', methods=['PUT'])
def update_student(id_param):
    try:
        student_id = int(id_param)
    except ValueError:
        return jsonify({"error": "L'ID doit être un nombre."}), 400

    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Étudiant non trouvé."}), 404

    data = request.get_json() or {}
    fn = data.get("firstName")
    ln = data.get("lastName")
    email = data.get("email")
    grade = data.get("grade")
    field = data.get("field")

    if not all([fn, ln, email, field]) or grade is None:
        return jsonify({"error": "Champs manquants."}), 400

    if len(fn) < 2 or len(ln) < 2 or not re.match(EMAIL_REGEX, str(email)):
        return jsonify({"error": "Données invalides."}), 400

    if not isinstance(grade, (int, float)) or isinstance(grade, bool) or not (0 <= grade <= 20):
        return jsonify({"error": "Données invalides."}), 400

    if field not in ALLOWED_FIELDS:
        return jsonify({"error": "Données invalides."}), 400

    if any(s["email"] == email and s["id"] != student_id for s in students_db):
        return jsonify({"error": "Email appartenant à un autre étudiant."}), 409

    student.update({
        "firstName": fn,
        "lastName": ln,
        "email": email,
        "grade": float(grade),
        "field": field
    })
    return jsonify(student), 200


@students_bp.route('/<id_param>', methods=['DELETE'])
def delete_student(id_param):
    try:
        student_id = int(id_param)
    except ValueError:
        return jsonify({"error": "L'ID doit être un nombre."}), 400

    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Étudiant non trouvé."}), 404

    students_db.remove(student)
    return jsonify({"message": "Supprimé avec succès."}), 200
