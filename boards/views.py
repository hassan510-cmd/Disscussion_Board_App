from django.shortcuts import render , get_object_or_404 ,redirect
from django.http import HttpResponse
from boards.models import Board ,Topic,Post
from django.contrib.auth.models import User
from .froms import AddNewBoard
from django.contrib.auth.decorators import login_required

# Create your views here.


last_user = User.objects.last()

@login_required
def home_page(request):
	# if request.user.is_anonymous:
	#
	# 	print(request.user.is_authenticated)
	# 	# return render(request,'login-page.html',{"message":"طيزك حمرا"})
	# 	return redirect('logout_page')
	print(request.user.is_authenticated)
	data=Board.objects.all().order_by("-id")

	posts_number=[]
	last_post_date=[]
	# print("enter method ")
	for bord in data:
		# print(bord.topics.all())
		# for topic in bord.topics.all():
		# 	posts_number.append(len(topic.posts.all()))
		# 	if topic.posts.last():
		#
		# 		last_post_date.append(topic.posts.last().created_date.strftime("%Y %m %d %I:%M:%S %p"))
		# 	else:
		# 		last_post_date.append("-")

		last_post_date=[topic.posts.last().created_date.strftime("%Y %m %d %I:%M:%S %p") if topic.posts.last() else "-" for topic in bord.topics.all()]
		posts_number=[len(x.posts.all()) for x in bord.topics.all()]
	last_topic_date = ["-" if str(x.topics.last())=='None' else x.topics.last().created_date.strftime("%Y %m %d %I:%M:%S %p") for x in data]
	# print(last_topic_date)
	if request.method=='POST':
		# board_name = request.POST['board_name']
		# board_desc = request.POST['desc']
		# Board.objects.create(name=board_name,description=board_desc)
		form=AddNewBoard(request.POST)
		if form.is_valid():
			board=form.save(commit=False)
		# Board.objects.create(name=form.cleaned_data.get('name'),
		#                      description=form.cleaned_data.get('description')
		#                      )
			board.name=form.cleaned_data.get('name')
			board.description=form.cleaned_data.get('description')
			board.save()
			# print(request.body)
			form = AddNewBoard()
			# print(form.cleaned_data.get('name'))
	else:
		form = AddNewBoard()
	data = Board.objects.all().order_by("-id")
	return render(
		request,"home_page.html",
		{
			'data':data,
			'last_topic_date':last_topic_date,
			'last_post_date':last_post_date,
			'post_num':posts_number,
			'form':form,
			'user':str(request.user).title()

		}
	)

@login_required
def topic_page(request,board_id):
	try:
		data=Board.objects.get(pk=board_id)
		topics = Topic.objects.filter(board=data.id).order_by('-created_date')
		# print(f"{request.path}".center("#", 50))
		# print(*dir(request),sep="\n")
	except Exception:
		return render(request,'404.html')
	return render(request,'all_topics.html',{"data":data,'topics':topics})

@login_required
def new_topic(request,board_id):
	try:
		data=Board.objects.get(pk=board_id)
		topics=Topic.objects.filter(board=data.id).order_by('-created_date')
		# print(f"{request.path}".center("#", 50))
		# print("ENTER NEW-TOPIC REQUEST".center(50, "*"))
		if request.method=='POST':
			# print("ENTER POST REQUEST".center(50,"*"))
			subject=request.POST['subject']
			message=request.POST['msg']

			topic=Topic.objects.create(subject=subject,board=data,created_by=request.user)
			post=Post.objects.create(msg=message,topic=topic,created_by=request.user)
			# print([subject,message,last_user,topic,post],"added successfully")
			# return redirect('topics',data.id)
	except Exception as e:
		print(e)
		return render(request,'404.html')
	return render(request,'add_new_topic.html',{'data':data,'topics':topics})

@login_required
def post_page(request,board_id,topic_id):
	try:
		# print("****************************")
		data = Board.objects.get(pk=board_id)
		post=Post.objects.filter(topic=topic_id).order_by("-id")
		print(f"{request.path}")
		# print("****************************")
		if request.method=='POST' and request.POST['post-content']!="":
			# print('hiiiiiii')
			post_content=request.POST['post-content']
			Post.objects.create(msg=post_content,topic_id=topic_id,created_by=request.user)
			print(request.POST['post-content'])

		# print(topic_id)
	except Exception as ex:
		print(ex)
		return render(request,'404.html')
	return render(request,'topic_posts.html',
	              {
		              'data':data,
		              'post':post,
		              'board_id':board_id,
		              'topic_id':topic_id,


	              }
	              )

@login_required
def delete_post(request,post_id):
	print(*dir(request),sep='\n')
	post=Post.objects.get(id=post_id)
	topic_id=Topic.objects.get(posts=post).id
	board_id=Board.objects.get(topics=topic_id).id

	post.delete()
	print(f'this is the id{post_id}\n topic_id{topic_id}\n board_id{board_id}')
	# print(f"{request.path}".center("#",50))
	return  post_page(request,board_id,topic_id)

# http://127.0.0.1:8000/boards_id/124/topic_id/71