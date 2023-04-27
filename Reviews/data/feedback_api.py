import datetime

from flask import jsonify, Blueprint, request

from . import db_session_rev
from .rev import Feedback

blueprint = Blueprint(
    'reviews_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    db_sess = db_session_rev.create_session()
    feedbacks = db_sess.query(Feedback).all()
    return jsonify(
        {
            'Feedbacks':
                [[item.id, item.name, item.estimation, item.comment, item.created_date, item.photo]
                 for item in feedbacks]
        }
    )


@blueprint.route('/api/feedback/<int:Feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    if feedback_id and type(feedback_id) == int:
        ids = []
        db_sess = db_session_rev.create_session()
        feedbacks = db_sess.query(Feedback).all()
        for feedback in feedbacks:
            ids.append(feedback.id)

        if feedback_id not in ids:
            return jsonify(
                {'Error': 'not such id in db'})
    else:
        return jsonify(
            {'Error': 'Bad request'})

    db_sess = db_session_rev.create_session()
    feedbacks = db_sess.query(Feedback).all()
    return jsonify(
        {
            'Feedback':
                [[item.id, item.name, item.estimation, item.comment, item.created_date, item.photo]
                 for item in feedbacks if item.id == feedback_id]
        }
    )


@blueprint.route('/api/add_feedback', methods=['POST'])
def add_feedback():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['name', 'estimation', 'comment']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session_rev.create_session()
    feedbacks = Feedback(
        name=request.json['name'],
        estimation=request.json['estimation'],
        comment=request.json['comment'],
        created_date=datetime.datetime.today(),
        photo='9.jpg',
    )
    db_sess.add(feedbacks)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/feedback_update/<int:update_id>', methods=['PUT'])
def update_feedback(update_id):
    if type(update_id) != int:
        return jsonify({'error': 'Not found'})

    db_sess = db_session_rev.create_session()
    feedbacks = db_sess.query(Feedback).all()
    ids = []
    for user in feedbacks:
        ids.append(user.id)

    if update_id not in ids:
        return jsonify({'error': 'Not such id in db'})

    if not request.json:
        return jsonify({'error': 'Empty request'})

    feedback_to_update = db_sess.query(Feedback).filter(Feedback.id == update_id).first()
    for key in request.json:
        if key == 'name':
            feedback_to_update.name = request.json['name']

        elif key == 'estimation':
            feedback_to_update.estimation = request.json['estimation']

        elif key == 'comment':
            feedback_to_update.comment = request.json['comment']

    db_sess.commit()
    return jsonify({'success': 'UPDATE'})


@blueprint.route('/api/del_feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    db_sess = db_session_rev.create_session()
    feedbacks = db_sess.query(Feedback).get(feedback_id)
    if not feedbacks:
        return jsonify({'error': 'Not found'})
    db_sess.delete(feedbacks)
    db_sess.commit()
    return jsonify({'success': 'DELETE'})
