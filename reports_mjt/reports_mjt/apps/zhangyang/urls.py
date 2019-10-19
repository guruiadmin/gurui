from django.conf.urls import url

from zhangyang import unionviews

urlpatterns = [
    # url(r'smallprogram$', ormviews.SmallProgram.as_view()),
    # url(r'smallprogram$', views.SmallProgram.as_view()),
    url(r'smallprogram$', unionviews.SmallProgram.as_view()),
]