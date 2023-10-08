import psycopg2
from flask import render_template, session

from Answers.answerform import AnswerForm
from Links import params
from settings import host, user, password, db_name


class Answers:
    @staticmethod
    def answers():
        form = AnswerForm()
        if form.validate_on_submit() and session.get("authorization"):
            try:
                connection = psycopg2.connect(
                    host=host, user=user, password=password, database=db_name
                )
                connection.autocommit = True

                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""INSERT INTO answers (user_id, answer) 
                            values
                            ('{session.get("id")}'::int, '{form.text.data}');"""
                    )

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            return "/answers"
        user_authorization = False
        if session.get("authorization"):
            user_authorization = True
        return render_template(
            "answers_page.html",
            **params,
            an_is_active="active",
            form=form,
            title="Answers",
            login=session.get("authorization"),
            user_authorization=user_authorization,
        )
