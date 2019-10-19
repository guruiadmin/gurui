from django.conf.urls import url

from lirui import logistics
from lirui import views

urlpatterns = [
    url(r'index$', views.OperationalData.as_view()),
    url(r'logis$', logistics.LogisticsApi.as_view()),
]
