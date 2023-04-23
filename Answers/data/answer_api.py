from flask import jsonify, Blueprint, request

from . import db_session_answers
from .answer_db import Answer_db

blueprint = Blueprint(
    'answer_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/answers', methods=['GET'])
def get_answers():
    db_sess = db_session_answers.create_session()
    answers = db_sess.query(Answer_db).all()
    return jsonify(
        {
            'answers':
                [[item.id, item.email, item.name, item.answer]
                 for item in answers]
        }
    )


@blueprint.route('/api/blog/<int:answer_id>', methods=['GET'])
def get_answer(answer_id):
    if answer_id and type(answer_id) == int:
        ids = []
        db_sess = db_session_answers.create_session()
        answers = db_sess.query(Answer_db).all()
        for answer in answers:
            ids.append(id)
        if answer_id not in ids:
            return jsonify(
                {'Error': 'not such id in db'})
    else:
        return jsonify(
            {'Error': 'Bad request'})

    db_sess = db_session_answers.create_session()
    answers = db_sess.query(Answer_db).all()
    return jsonify(
        {
            'answers':
                [[item.id, item.email, item.name, item.answer]
                 for item in answers if item.id == answer_id]
        }
    )


@blueprint.route('/api/add_answer', methods=['POST'])
def add_answer():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'email', 'name', 'answer']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session_answers.create_session()
    answers = Answer_db(
        email=request.json['email'],
        name=request.json['name'],
        answer=request.json['answer']
    )
    db_sess.add(answers)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/answer_update/<int:update_id>', methods=['PUT'])
def update_answer(update_id):
    if type(update_id) != int:
        return jsonify({'error': 'Not found'})

    db_sess = db_session_answers.create_session()
    answers = db_sess.query(Answer_db).all()
    ids = []
    for answer in answers:
        ids.append(answer.id)

    if update_id not in ids:
        return jsonify({'error': 'Not such id in db'})

    if not request.json:
        return jsonify({'error': 'Empty request'})

    answer_to_update = db_sess.query(Answer_db).filter(answer.id == update_id).first()
    for key in request.json:
        if key == 'email':
            answer_to_update.email = request.json['email']

        elif key == 'name':
            answer_to_update.name = request.json['name']

        elif key == 'answer':
            answer_to_update.answer = request.json['answer']

    db_sess.commit()
    return jsonify({'success': 'UPDATE'})


@blueprint.route('/api/del_answer/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    db_sess = db_session_answers.create_session()
    answers = db_sess.query(Answer_db).get(answer_id)
    if not answers:
        return jsonify({'error': 'Not found'})
    db_sess.delete(answers)
    db_sess.commit()
    return jsonify({'success': 'DELETE'})
