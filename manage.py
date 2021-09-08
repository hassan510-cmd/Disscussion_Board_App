#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discussion_board.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# to run single line you must run the manage.py file in python console
# by right click and select run file in python console then start you code




# import jinja2
# env = jinja2.Environment()
# env.globals.update(zip=zip)

# from django.contrib.auth.models import User
# from boards.models import Board ,Topic,Post
# b=Board.objects.all()
# t=Topic.objects.all()
# t.posts.all()
# p=Post.objects.all()
# x=zip(b,t,p)
# # x
# for i in x:
#     for j in i:
#         print(j)
# for bord in b:
#     # print(bord.topics.all())
#     for topic in bord.topics.all():
#         print(topic)
#
#         print(len(topic.posts.all()))
# txt="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ad blanditiis culpa, eius inventore ipsum nam nemo nihil odit omnis optio porro quam quas quos tenetur ut vel veniam voluptatum? Id!"
# boadr1=Board(name='php language',description=txt)
# boadr1.save()
# boadr1.id
# boadr1.name
# Board.objects.all()[1].name
# for i in Board.objects.all():
#     print(i.name)
#
# last_user=User.objects.last()
#
# last_user.username
#
# Topic.objects.filter(board=0)




# b=Board.objects.all()
# Topic.objects.posts.all()
# x=b.topics.all()
# Post.objects.posts
# for i in x:
#     print(i.posts.last().created_date.strftime("%Y %m %d %I:%M:%S"))
# Topic.objects.filter(board=b)
# t=Topic.objects.get(pk=2)
# t.posts.all()
# Post.objects.create()