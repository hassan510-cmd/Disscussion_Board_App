from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_view
urlpatterns=[
	path('signup/',views.sign_up,name='signup'),
	# path('login-page/',views.login_page,name='login_page'),
	path('login-page/', auth_view.LoginView.as_view(template_name='login-page.html'), name='login_page'),
	# path('logout-page/',auth_view.LogoutView.as_view(template_name='login-page.html'),name='logout_page'),
	path('logout-page/',views.logout_page,name='logout_page'),
	path('UserSetting/',auth_view.PasswordChangeView.as_view(template_name="user-setting.html"),name='user_setting'),
	path("password_change_done/",auth_view.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),name="password_change_done")
]