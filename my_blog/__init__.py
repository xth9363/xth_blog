# Celery相关
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# celery_conf 是我们自定义的文件
from .celery_conf import app as celery_app


__all__ = ['celery_app']
# Celery相关结束
