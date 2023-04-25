import os

from settings import GENERAL_NAME_LINK

reviews = f'{GENERAL_NAME_LINK}/reviews'
events = f'{GENERAL_NAME_LINK}/events'
event = f'{GENERAL_NAME_LINK}/event'
blog = f'{GENERAL_NAME_LINK}/blog'
authorization = f'{GENERAL_NAME_LINK}/authorization'
answers = f'{GENERAL_NAME_LINK}/answers'
about_us = f'{GENERAL_NAME_LINK}/about_us'
general = f'{GENERAL_NAME_LINK}/'
register = f'{GENERAL_NAME_LINK}/register'
blog_Admin = f'{GENERAL_NAME_LINK}/blog_admin'
event_Admin = f'{GENERAL_NAME_LINK}/event_admin'
answers_Admin = f'{GENERAL_NAME_LINK}/answers_admin'
cabinet = f'{GENERAL_NAME_LINK}/cabinet'
logout = f'{GENERAL_NAME_LINK}/cabinet/logout'
delete = f'{GENERAL_NAME_LINK}/cabinet/delete'
reviews_Admin = f'{GENERAL_NAME_LINK}/reviews_admin'
photo_add_Admin = f'{GENERAL_NAME_LINK}/add_photo_admin'
types = f'{GENERAL_NAME_LINK}/event/types'
params = {'general': general, 'about_us': about_us, 'blog': blog, 'reviews': reviews,
          'answers': answers, 'events': events, 'authorization': authorization, 'cabinet': cabinet}
params_admin = {'photo_add_Admin': photo_add_Admin, 'reviews_Admin': reviews_Admin, 'answers_Admin': answers_Admin,
                'event_Admin': event_Admin, 'blog_Admin': blog_Admin, 'general': general}

