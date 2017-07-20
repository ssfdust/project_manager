from backend import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^islogin/', views.is_login),
    url(r'^get_frontend_status[/]*', views.get_frontend_status)
]
