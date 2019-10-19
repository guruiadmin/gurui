from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from public import views
from public import classviews

urlpatterns = [
    url(r'public$', views.ManageData.as_view()),#后台系统首页统计
    # url(r'publico$', classviews.ManageData.as_view()),#后台系统首页统计
]
# # 定义视图集的路由
router = DefaultRouter()
router.register(r'publico', classviews.ManageData, base_name='manage')
router.register('skus/search', views.SKUSearchViewSet, base_name='skus_search')
# 将视图集的路由添加到urlpatterns
urlpatterns += router.urls