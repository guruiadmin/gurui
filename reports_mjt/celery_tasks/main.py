from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reports_mjt.settings.dev'

# 创建celery应用
app = Celery('mingjingtai')

# 导入celery配置
app.config_from_object('celery_tasks.config')

