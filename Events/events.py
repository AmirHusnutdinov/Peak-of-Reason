from flask import render_template
import math
from Links import about_us, blog, reviews, answers, event1, \
    event2, event3, event4, authorization, general, cabinet, events


class Events:
    @staticmethod
    def events(events_lst):
        count_of_columns = math.ceil(len(events_lst) / 3)
        count_of_posts = len(events_lst)

        three_posts = []

        start = 0
        end = 3
        blog_inform = events_lst[::-1]
        for i in range(count_of_columns):
            three_posts.append(blog_inform[start:end])

            if start + 3 <= count_of_posts:
                start += 3

            if end + 3 <= count_of_posts:
                end += 3

            elif end + 2 <= count_of_posts:
                end += 2

            elif end + 1 <= count_of_posts:
                end += 1

        return render_template('events.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               event1=event1,
                               event2=event2,
                               authorization=authorization,
                               cabinet=cabinet,
                               posts=three_posts)

    @staticmethod
    def event1(events1):
        count_of_columns = math.ceil(len(events1) / 3)
        count_of_posts = len(events1)

        three_posts = []

        start = 0
        end = 3
        blog_inform = events1[::-1]
        for i in range(count_of_columns):
            three_posts.append(blog_inform[start:end])

            if start + 3 <= count_of_posts:
                start += 3

            if end + 3 <= count_of_posts:
                end += 3

            elif end + 2 <= count_of_posts:
                end += 2

            elif end + 1 <= count_of_posts:
                end += 1

        return render_template('event1.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event2=event2,
                               event3=event3,
                               event4=event4,
                               authorization=authorization,
                               cabinet=cabinet,
                               posts=three_posts)

    @staticmethod
    def event2(events2):
        count_of_columns = math.ceil(len(events2) / 3)
        count_of_posts = len(events2)

        three_posts = []

        start = 0
        end = 3
        blog_inform = events2[::-1]
        for i in range(count_of_columns):
            three_posts.append(blog_inform[start:end])

            if start + 3 <= count_of_posts:
                start += 3

            if end + 3 <= count_of_posts:
                end += 3

            elif end + 2 <= count_of_posts:
                end += 2

            elif end + 1 <= count_of_posts:
                end += 1

        return render_template('event2.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               event3=event3,
                               event4=event4,
                               posts=three_posts,
                               authorization=authorization,
                               cabinet=cabinet
                               )
