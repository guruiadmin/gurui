from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from wangpengfei import help_duration

urlpatterns = [
    url(r'wpf$', help_duration.Activity.as_view()),
]


