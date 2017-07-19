from backend import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^islogin/', views.is_login)
]
