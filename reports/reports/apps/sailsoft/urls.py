from django.conf.urls import url

from sailsoft import views

urlpatterns = [
    url(r'index$', views.GuRui.as_view()),
]