from flask import jsonify, Blueprint, request

from . import db_session_blog
from .Post import Post

blueprint = Blueprint(
    'blog_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/blog', method=['GET'])
def get_posts():
    db_sess = db_session_blog.create_session()
    posts = db_sess.query(Post).all()
    return jsonify(
        {
            'posts':
                [[item.id, item.photo_name, item.name, item.link, item.created_date, item.post_text]
                 for item in posts]
        }
    )


@blueprint.route('/api/blog/<int:post_id>', method=['GET'])
def get_posts(post_id):
    if post_id and type(post_id) == int:
        ids = []
        db_sess = db_session_blog.create_session()
        posts = db_sess.query(Post).all()
        for post in posts:
            ids.append(id)
        if post_id not in ids:
            return jsonify(
                {'Error': 'not such id in db'})
    else:
        return jsonify(
            {'Error': 'Bad request'})

    db_sess = db_session_blog.create_session()
    posts = db_sess.query(Post).all()
    return jsonify(
        {
            'posts':
                [[item.id, item.photo_name, item.name, item.link, item.created_date, item.post_text]
                 for item in posts if item.id == post_id]
        }
    )


@blueprint.route('/api/add_post', methods=['POST'])
def add_post():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['id', 'photo_name', 'name', 'signature', 'link', 'created_date', 'post_text']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session_blog.create_session()
    posts = Post(
        photo_name=request.json['photo_name'],
        name=request.json['name'],
        signature=request.json['signature'],
        link=request.json['link'],
        created_date=request.json['created_date'],
        post_text=request.json['post_text']
    )
    db_sess.add(posts)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/post_update/<int:update_id>', methods=['PUT'])
def update_post(update_id):
    if type(update_id) != int:
        return jsonify({'error': 'Not found'})

    db_sess = db_session_blog.create_session()
    posts = db_sess.query(Post).all()
    ids = []
    for user in posts:
        ids.append(user.id)

    if update_id not in ids:
        return jsonify({'error': 'Not such id in db'})

    if not request.json:
        return jsonify({'error': 'Empty request'})

    post_to_update = db_sess.query(Post).filter(Post.id == update_id).first()
    for key in request.json:
        if key == 'photo_name':
            post_to_update.photo_name = request.json['photo_name']

        elif key == 'name':
            post_to_update.name = request.json['name']

        elif key == 'signature':
            post_to_update.signature = request.json['signature']

        elif key == 'link':
            post_to_update.link = request.json['link']

        elif key == 'created_date':
            post_to_update.created_date = request.json['created_date']

        elif key == 'post_text':
            post_to_update.post_text = request.json['post_text']

    db_sess.commit()
    return jsonify({'success': 'UPDATE'})


@blueprint.route('/api/del_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    db_sess = db_session_blog.create_session()
    posts = db_sess.query(Post).get(post_id)
    if not posts:
        return jsonify({'error': 'Not found'})
    db_sess.delete(posts)
    db_sess.commit()
    return jsonify({'success': 'DELETE'})
