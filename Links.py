import os

host = '0.0.0.0'
port = int(os.environ.get("PORT", 5000))
reviews = f'http://{host}:{port}/reviews'
events = f'http://{host}:{port}/events'
event = f'http://{host}:{port}/event'
blog = f'http://{host}:{port}/blog'
authorization = f'http://{host}:{port}/authorization'
answers = f'http://{host}:{port}/answers'
about_us = f'http://{host}:{port}/about_us'
general = f'http://{host}:{port}'
register = f'http://{host}:{port}/register'
blog_Admin = f'http://{host}:{port}/blog_admin'
event_Admin = f'http://{host}:{port}/event_admin'
answers_Admin = f'http://{host}:{port}/answers_admin'
cabinet = f'http://{host}:{port}/cabinet'
logout = f'http://{host}:{port}/cabinet/logout'
delete = f'http://{host}:{port}/cabinet/delete'
reviews_Admin = f'http://{host}:{port}/reviews_admin'
photo_add_Admin = f'http://{host}:{port}/add_photo_admin'
types = f'http://{host}:{port}/event/types'
params = {'general': general, 'about_us': about_us, 'blog': blog, 'reviews': reviews,
          'answers': answers, 'events': events, 'authorization': authorization, 'cabinet': cabinet}
params_admin = {'photo_add_Admin': photo_add_Admin, 'reviews_Admin': reviews_Admin, 'answers_Admin': answers_Admin,
                'event_Admin': event_Admin, 'blog_Admin': blog_Admin, 'general': general}

