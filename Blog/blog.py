from flask import render_template
from Links import about_us, blog, reviews, answers, event1, authorization, general, cabinet
import math


class Blog:
    @staticmethod
    def blog(blog_inform):

        count_of_colums = math.ceil(len(blog_inform) / 3)
        count_of_posts = len(blog_inform)

        three_posts = []

        start = 0
        end = 3
        blog_inform = blog_inform[::-1]
        for i in range(count_of_colums):
            three_posts.append(blog_inform[start:end])

            if start + 3 <= count_of_posts:
                start += 3

            if end + 3 <= count_of_posts:
                end += 3

            elif end + 2 <= count_of_posts:
                end += 2

            elif end + 1 <= count_of_posts:
                end += 1

        return render_template('blog_page.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               authorization=authorization,
                               posts=three_posts,
                               cabinet=cabinet
                               )

    @staticmethod
    def blog_pages(item):
        return render_template('blog_page_example.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               authorization=authorization,
                               cabinet=cabinet,
                               name=item[2],
                               signature=item[3],
                               date=item[5],
                               photo_name=item[1],
                               text=item[6])
