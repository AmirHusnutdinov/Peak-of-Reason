from flask import jsonify, Blueprint, request

from . import db_session_event
from .all_events import All_events

blueprint = Blueprint(
    'event_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/events', methods=['GET'])
def get_events():
    db_sess = db_session_event.create_session()
    events = db_sess.query(All_events).all()
    return jsonify(
        {
            'events':
                [[item.id, item.photo_name, item.name, item.signature, item.link, item.created_date]
                 for item in events]
        }
    )


@blueprint.route('/api/blog/<int:event_id>', methods=['GET'])
def get_event(event_id):
    if event_id and type(event_id) == int:
        ids = []
        db_sess = db_session_event.create_session()
        events = db_sess.query(All_events).all()
        for event in events:
            ids.append(id)
        if event_id not in ids:
            return jsonify(
                {'Error': 'not such id in db'})
    else:
        return jsonify(
            {'Error': 'Bad request'})

    db_sess = db_session_event.create_session()
    events = db_sess.query(All_events).all()
    return jsonify(
        {
            'events':
                [[item.id, item.photo_name, item.name, item.signature, item.link, item.created_date]
                 for item in events if item.id == event_id]
        }
    )


@blueprint.route('/api/add_event', methods=['POST'])
def add_event():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'photo_name', 'name', 'signature', 'link', 'created_date']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session_event.create_session()
    events = All_events(
        photo_name=request.json['photo_name'],
        name=request.json['name'],
        signature=request.json['signature'],
        link=request.json['link'],
        created_date=request.json['created_date'],
        post_text=request.json['post_text']
    )
    db_sess.add(events)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/event_update/<int:update_id>', methods=['PUT'])
def update_event(update_id):
    if type(update_id) != int:
        return jsonify({'error': 'Not found'})

    db_sess = db_session_event.create_session()
    events = db_sess.query(All_events).all()
    ids = []
    for event in events:
        ids.append(event.id)

    if update_id not in ids:
        return jsonify({'error': 'Not such id in db'})

    if not request.json:
        return jsonify({'error': 'Empty request'})

    event_to_update = db_sess.query(All_events).filter(event.id == update_id).first()
    for key in request.json:
        if key == 'photo_name':
            event_to_update.photo_name = request.json['photo_name']

        elif key == 'name':
            event_to_update.name = request.json['name']

        elif key == 'signature':
            event_to_update.signature = request.json['signature']

        elif key == 'link':
            event_to_update.link = request.json['link']

        elif key == 'created_date':
            event_to_update.created_date = request.json['created_date']

        elif key == 'post_text':
            event_to_update.post_text = request.json['post_text']

    db_sess.commit()
    return jsonify({'success': 'UPDATE'})


@blueprint.route('/api/del_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    db_sess = db_session_event.create_session()
    events = db_sess.query(All_events).get(event_id)
    if not events:
        return jsonify({'error': 'Not found'})
    db_sess.delete(events)
    db_sess.commit()
    return jsonify({'success': 'DELETE'})
