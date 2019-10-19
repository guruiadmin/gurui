from django.conf.urls import url

from luweifeng import text
from luweifeng import views

urlpatterns = [
    url(r'mjt$', views.PersonQuery.as_view()),
    url(r'test$', text.ActiPersonQuery.as_view()),
]