from flask import render_template, request
from Links import blog_Admin, event_Admin, answers_Admin, reviews_Admin, general, photo_add_Admin


class Admin:
    @staticmethod
    def admin(method):
        if method == 'GET':
            return render_template('admin_page.html',
                                   general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin,
                                   photo_add_Admin=photo_add_Admin
                                   )
        elif method == 'POST':
            return [
                    request.form['inp1'],
                    request.form['inp2'],
                    request.form['inp3'],
                    request.form['inp4'],
                    request.form['inp5']]

    @staticmethod
    def admin_answers(method, answers):
        len_ans = len(answers)
        if method == 'GET':
            return render_template('admin_answers_page.html',
                                   general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin,
                                   answers=answers,
                                   remained=len_ans,
                                   photo_add_Admin=photo_add_Admin
                                   )
        elif method == 'POST':
            return [request.form['inp1']]

    @staticmethod
    def admin_rev(method, rev):
        len_rev = len(rev)
        if method == 'GET':
            return render_template('rev_admin_page.html',
                                   general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin,
                                   review=rev,
                                   remained=len_rev,
                                   photo_add_Admin=photo_add_Admin)
        elif method == 'POST':
            return [rev, (request.form['inp1']).split(), (request.form['inp2']).split()]

    @staticmethod
    def add_photo(method):
        if method == 'GET':
            return render_template('add_new_image.html', general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin,
                                   photo_add_Admin=photo_add_Admin)
        elif method == 'POST':
            return request.files

    @staticmethod
    def event_admin(method):
        if method == 'GET':
            return render_template('admin_event.html',
                                   general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin,
                                   photo_add_Admin=photo_add_Admin
                                   )
        elif method == 'POST':
            return [request.form['inp0'],
                    request.form['inp1'],
                    request.form['inp2'],
                    request.form['inp3'],
                    request.form['inp4'],
                    request.form['inp5']]
