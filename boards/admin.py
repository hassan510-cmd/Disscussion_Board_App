from django.contrib import admin
from .models import Board ,Topic ,Post
from django.contrib.auth.models import Group
# Register your models here.

admin.site.site_header='Hassan custom change'
admin.site.site_title='Hassan custom change2'

class container(admin.StackedInline):
    model = Topic
    extra = 1

class BoardAdmin(admin.ModelAdmin):
    inlines = [container]


class TopicAdmin(admin.ModelAdmin):
    # fields = ('subject',)
    list_display = ('subject','board','concate_sub_board')
    list_display_links = ('concate_sub_board',)
    list_editable = ('subject',)
    list_filter = ('board',)
    search_fields = ('subject',)


    def concate_sub_board(self,obj):
        return f"{obj.subject}=>{obj.board}"
    # pass
admin.site.register(Board,BoardAdmin)


admin.site.register(Topic,TopicAdmin)
admin.site.register(Post)
admin.site.unregister(Group)
