import django.shortcuts
from django.shortcuts import render , get_object_or_404 ,redirect
from django.http import HttpResponse
from boards.models import Board ,Topic,Post
from django.contrib.auth.models import User
from .froms import AddNewBoard
from django.db.models import Count , F
from django.contrib.auth.decorators import login_required

# Create your views here.
last_user = User.objects.last()

@login_required
def home_page(request):
	data=Board.get_all_boards()

	# posts_number=[]
	# last_post_date=[]
	# for bord in data:
	#
	# 	last_post_date=[topic.posts.last().created_date.strftime("%Y %m %d %I:%M:%S %p") if topic.posts.last() else "-" for topic in bord.topics.all()]
		# posts_number=[len(x.posts.all()) for x in bord.topics.all()]
		# posts_number.append(Post.objects.filter(topic__board=bord).count())
		# print(posts_number)
	# last_topic_date = ["-" if str(x.topics.last())=='None' else x.topics.last().created_date.strftime("%Y %m %d %I:%M:%S %p") for x in data]
	# print(last_topic_date)
	if request.method=='POST':
		form=AddNewBoard(request.POST)
		if form.is_valid():
			board=form.save(commit=False)
			board.name=form.cleaned_data.get('name')
			board.description=form.cleaned_data.get('description')
			board.save()
			form = AddNewBoard()
	else:
		form = AddNewBoard()
	data = Board.get_all_boards()
	return render(
		request,"home_page.html",
		{
			'data':data,
			'form':form,
			'user':request.user
		}
	)

@login_required
def topic_page(request,board_id):
	try:
		data=Board.objects.get(pk=board_id)
		topics = Topic.objects.filter(board=data.id).order_by('-created_date').annotate(posts_num=Count('posts'))
	except Exception:
		return render(request,'404.html')
	return render(request,'all_topics.html',{"data":data,'topics':topics})

@login_required
def new_topic(request,board_id):
	try:
		data=Board.objects.get(pk=board_id)
		topics=Topic.objects.filter(board=data.id).order_by('-created_date')
		if request.method=='POST':
			subject=request.POST['subject']
			message=request.POST['msg']
			topic=Topic.objects.create(subject=subject,board=data,created_by=request.user)
			post=Post.objects.create(msg=message,topic=topic,created_by=request.user)
	except Exception as e:
		print(e)
		return render(request,'404.html')
	return render(request,'add_new_topic.html',{'data':data,'topics':topics})

@login_required
def post_page(request,board_id,topic_id):
	try:
		data = Board.objects.get(pk=board_id)
		post=Post.objects.filter(topic=topic_id).order_by("-id")
		topic_name=Topic.objects.get(pk=topic_id).subject
		Topic.objects.filter(pk=topic_id).update(views=F('views')+1)
		if request.method=='POST' and request.POST['post-content']!="":
			post_content=request.POST['post-content']
			Post.objects.create(msg=post_content,topic_id=topic_id,created_by=request.user)
	except Exception as ex:
		print(ex)
		return render(request,'404.html')
	return render(request,'topic_posts.html',
	              {
		            'data':data,
		            'post':post,
		            'board_id':board_id,
		            'topic_id':topic_id,
					"topic_name":topic_name
	              }
	              )

@login_required
def delete_post(request,post_id):
	post=Post.objects.get(id=post_id)
	topic_id=Topic.objects.get(posts=post).id
	board_id=Board.objects.get(topics=topic_id).id
	post.delete()
	return  post_page(request,board_id,topic_id)

# http://127.0.0.1:8000/boards_id/124/topic_id/71

# import requests
# requests.get(url="http://127.0.0.1:8000/home/")