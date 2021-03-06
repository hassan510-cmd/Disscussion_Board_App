from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from .froms import AddNewBoard
from django.db.models import Count, F
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

last_user = User.objects.last()


# @login_required
# def home_page(request):
# 	data=Board.get_all_boards()
# 	if request.method=='POST':
# 		form=AddNewBoard(request.POST)
# 		if form.is_valid():
# 			board=form.save(commit=False)
# 			board.name=form.cleaned_data.get('name')
# 			board.description=form.cleaned_data.get('description')
# 			board.save()
# 			form = AddNewBoard()
# 	else:
# 		form = AddNewBoard()
# 	data = Board.get_all_boards()
# 	return render(
# 		request,"home_page.html",
# 		{
# 			'data':data,
# 			'form':form,
# 			'user':request.user
# 		}
# 	)

class HomePage(View):
    def __init__(self):
        self.data = ''
        self.pages_num = 0

    def refresh_data(self):
        self.data = Board.get_all_boards().order_by('id')

    def render(self, request, form):
        paginator = Paginator(self.data, 5)
        self.pages_num = paginator.num_pages
        try:
            page = request.GET.get('page', 1)
            self.data = paginator.page(page)
        except PageNotAnInteger:
            self.data = paginator.page(1)
        except EmptyPage:
            self.data = paginator.page(self.pages_num)
        try:
            current_page_number = int(request.META['QUERY_STRING'].split("=")[1])
        except Exception:
            current_page_number = 1
        next_page_number = current_page_number + 1 if current_page_number + 1 <= self.pages_num else self.pages_num
        previous_page_number = current_page_number - 1 if current_page_number - 1 >= 1 else 1

        return render(
            request, "home_page.html",
            {
                'data': self.data,
                'form': form,
                'user': request.user,
                'pages_number': list(paginator.page_range),
                'previous_page_number': previous_page_number,
                'next_page_number': next_page_number,
                'current_page_number': current_page_number
            }
        )

    def post(self, request):
        form = AddNewBoard(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.name = form.cleaned_data.get('name')
            board.description = form.cleaned_data.get('description')
            board.save()
            form = AddNewBoard()
        self.refresh_data()
        return self.render(request, form)

    def get(self, request):
        form = AddNewBoard()
        self.refresh_data()
        return self.render(request, form)


@login_required
def topic_page(request, board_id):
    try:
        data = Board.objects.get(pk=board_id)
        topics = Topic.objects.filter(board=data.id).order_by('-created_date').annotate(posts_num=Count('posts'))
    except Exception:
        return render(request, '404.html')
    return render(request, 'all_topics.html', {"data": data, 'topics': topics})


@login_required
def new_topic(request, board_id):
    try:
        data = Board.objects.get(pk=board_id)
        topics = Topic.objects.filter(board=data.id).order_by('-created_date')
        if request.method == 'POST':
            subject = request.POST['subject']
            message = request.POST['msg']
            topic = Topic.objects.create(subject=subject, board=data, created_by=request.user)
            post = Post.objects.create(msg=message, topic=topic, created_by=request.user)
    except Exception as e:
        print(e)
        return render(request, '404.html')
    return render(request, 'add_new_topic.html', {'data': data, 'topics': topics})


@login_required
def post_page(request, board_id, topic_id):
    try:
        data = Board.objects.get(pk=board_id)
        post = Post.objects.filter(topic=topic_id).order_by("-id")
        topic_name = Topic.objects.get(pk=topic_id).subject
        Topic.objects.filter(pk=topic_id).update(views=F('views') + 1)
        if request.method == 'POST' and request.POST['post-content'] != "":
            post_content = request.POST['post-content']
            Post.objects.create(msg=post_content, topic_id=topic_id, created_by=request.user)
    except Exception as ex:
        print(ex)
        return render(request, '404.html')
    return render(request, 'topic_posts.html',
                  {
                      'data': data,
                      'post': post,
                      'board_id': board_id,
                      'topic_id': topic_id,
                      "topic_name": topic_name
                  }
                  )


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return post_page(request, post.topic.board.pk, post.topic.pk)


@method_decorator(login_required, name='dispatch')
class EditPost(UpdateView):
    model = Post
    fields = ("msg",)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.edit_date = timezone.now()
        post.save()
        print(request)
        return redirect('topic_page', board_id=post.topic.board.pk, topic_id=post.topic.pk)

# http://127.0.0.1:8000/boards_id/124/topic_id/71

# import requests
# requests.get(url="http://127.0.0.1:8000/home/")
