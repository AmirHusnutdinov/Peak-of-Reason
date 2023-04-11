from flask import render_template
import math
from Links import about_us, blog, reviews, answers, event, \
    authorization, general, cabinet, events, types


class Events:
    @staticmethod
    def three_posts_funk(events_lst):
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
        return three_posts

    @staticmethod
    def events(events_lst, file):
        three_posts = Events.three_posts_funk(events_lst)
        event1 = event + '/?teen=1'
        event2 = event + '/?adult=1'
        if not file:
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
        else:
            return render_template(file,
                                   general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   events=events,
                                   authorization=authorization,
                                   cabinet=cabinet)

    @staticmethod
    def event(events1, mode):
        three_posts = Events.three_posts_funk(events1)
        pb = ''
        tt = ''
        orator = ''
        file = ''

        if mode == 'teen':
            pb = types + '/?pb=1'
            tt = types + '/?tt=1'
            orator = types + '/?orator=1'
            file = 'event1.html'

        elif mode == 'adult':
            pb = types + '/?tp=1'
            tt = types + '/?ic=1'
            orator = types + '/?ac=1'
            file = 'event2.html'

        return render_template(file,
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               pb=pb,
                               tt=tt,
                               orator=orator,
                               authorization=authorization,
                               cabinet=cabinet,
                               posts=three_posts)

    @staticmethod
    def types_of_events(events_type, label):
        three_posts = Events.three_posts_funk(events_type)
        return render_template('types.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               posts=three_posts,
                               authorization=authorization,
                               cabinet=cabinet,
                               label=label
                               )
