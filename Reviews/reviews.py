from flask import render_template, session
from Links import params
from database_query import database_query
from Reviews.reviewsform import ReviewsForm
from Blog.blog import make_date


class Reviews:
    @staticmethod
    def reviews(mode):
        form = ReviewsForm()
        user_authorization = False
        if session.get("authorization"):
            user_authorization = True
        if mode == 'GET':
            rand_list = database_query("""select users.name, estimation, comment, to_char(created_date, 'dd Mon YYYY'),
                 feedback.photo_way from feedback INNER JOIN users ON feedback.user_id = users.user_id
                 order by random() limit 4;""")
            rand_list = list(map(list, rand_list))
            for i in range(len(rand_list)):
                rand_list[i][3] = make_date(rand_list[i][3])
            return render_template(
                "reviews/reviews_page.html",
                **params,
                reviews_=rand_list,
                re_is_active="active",
                form=form,
                title="Отзывы",
                login=session.get("authorization"),
                user_authorization=user_authorization,
            )
        elif mode == 'POST':
            user_id = int(session.get("id"))
            print(user_id)
            date = str(database_query("""SELECT to_char(current_date, 'dd Mon YYYY');""")[0])[2:-3]
            if form.validate_on_submit() and session.get("authorization"):
                database_query(f"""INSERT INTO feedback_to_moderate (user_id, estimation, comment, created_date) 
                                values ({user_id}, {int(form.prof.data)}, '{form.text.data}', '{date}'::date)""")
                return "/reviews"
