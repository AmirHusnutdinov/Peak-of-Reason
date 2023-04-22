from flask import jsonify, Blueprint

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
