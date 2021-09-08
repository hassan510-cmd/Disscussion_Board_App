from django.urls import path
from boards import views
urlpatterns = [
    path('home/',views.home_page,name='home'),
	path('boards_id/<board_id>/',views.topic_page,name='topics'),
	path('boards_id/<board_id>/new/',views.new_topic,name='new_topic'),
	path('boards_id/<board_id>/topic_id/<topic_id>',views.post_page,name='topic_page'),
	path('delete-post/<post_id>',views.delete_post,name='del_post'),

]