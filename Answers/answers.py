from flask import render_template

from Answers.answerform import AnswerForm
from Links import params


class Answers:
    @staticmethod
    def answers():
        form = AnswerForm()
        if form.validate_on_submit():
            return [form.email.data, form.name.data, form.text.data]
        return render_template('answers_page.html', **params,
                               an_is_active='active', form=form,
                               title='Answers')
