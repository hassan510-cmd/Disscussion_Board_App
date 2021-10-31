from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
	name=models.CharField(max_length=50,unique=True)
	description=models.CharField(max_length=300)

	def count_posts(self):
		count=Post.objects.filter(topic__board=self).count()
		# print(count,"///")
		return count

	def get_last_post_date(self):

		last_date=[topic.posts.last().created_date.strftime("%Y %m %d %I:%M:%S %p") if topic.posts.last() else "-" for topic in self.topics.all()]

		if len(last_date)>=1:
			return last_date[-1]
		else:
			return "no posts yet"

	def get_last_topic_date(self):
		if self.topics.last():
			last_topic_date=self.topics.last().created_date.strftime("%Y %m %d %I:%M:%S %p")
		else:
			last_topic_date="no topics yet"
		return last_topic_date

	@staticmethod
	def get_all_boards():
		return Board.objects.all().order_by(f"-id")

	def __str__(self):
		return self.name
class Topic(models.Model):
	subject= models.CharField(max_length=500)
	board= models.ForeignKey(Board,related_name='topics',on_delete=models.CASCADE)
	created_by= models.ForeignKey(User,related_name='topics',on_delete=models.CASCADE)
	created_date= models.DateTimeField(auto_now_add=True)
	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.subject



	# def count_topic_posts(self):
	# 	topic = Topic.objects.filter(board=1).order_by('-created_date')
	#
	# 	for i in topic:
	# 		posts_num=i.posts.all().count()
	# 		print(posts_num)
class Post(models.Model):

	msg=models.TextField(max_length=3000)
	topic=models.ForeignKey(Topic,related_name='posts',on_delete=models.CASCADE)
	created_by=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
	created_date=models.DateTimeField(auto_now_add=True)
	views = models.PositiveIntegerField(default=0)
	edit_date=models.DateTimeField(null=True)


class comment(models.Model):
	comment=models.CharField(max_length=1000)
	related_post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
	likes=models.PositiveIntegerField(default=0)
	dislikes=models.PositiveIntegerField(default=0)


class reply(models.Model):
	reply=models.CharField(max_length=1000)
	comment=models.ForeignKey(comment,related_name='replies',on_delete=models.CASCADE)
	likes=models.PositiveIntegerField(default=0)
	dislikes=models.PositiveIntegerField(default=0)

