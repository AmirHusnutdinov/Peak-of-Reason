from flask import render_template, session
from database_query import database_query
from Answers.answerform import AnswerForm
from Links import params, authorization


class Answers:
    @staticmethod
    def answers():
        form = AnswerForm()
        if form.validate_on_submit() and session.get("authorization"):
            database_query(f"""INSERT INTO answers (user_id, answer) 
                            values('{session.get("id")}'::int, '{form.text.data}');""")
            return "/answers"
        user_authorization = False
        if session.get("authorization"):
            user_authorization = True
        return render_template(
            "answers/answers_page.html",
            **params,
            an_is_active="active",
            form=form,
            authorization_link=authorization,
            title="Вопросы",
            login=session.get("authorization"),
            user_authorization=user_authorization,
        )
