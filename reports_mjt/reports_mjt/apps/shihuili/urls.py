from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from shihuili import activity
from shihuili import finance
from shihuili import manage
from shihuili import reportsa
from shihuili import views

urlpatterns = [
    url(r'index$', views.SystemHomePage.as_view()),#后台系统首页统计
    url(r'manage$', manage.ClaOrganizationViewSeet.as_view()),#manage路径
    url(r'acti$', activity.ActiPersonQuery.as_view()),
    url(r'reports$', reportsa.Organization.as_view()),#shops路径
]
# # 定义视图集的路由
router = DefaultRouter()
router.register(r'finance', finance.FinanceClass, base_name='manage')
# 将视图集的路由添加到urlpatterns
urlpatterns += router.urls
