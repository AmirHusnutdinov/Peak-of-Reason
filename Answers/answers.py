from flask import render_template, request
from Links import params


class Answers:
    @staticmethod
    def answers(method):
        if method == 'GET':
            return render_template('answers_page.html', **params,
                                   an_is_active='active')
        elif method == 'POST':
            return [request.form['inp1'], request.form['inp2'], request.form['inp3']]
