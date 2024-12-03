from django.urls import path, re_path

from .views import ProbableFightView

app_name = 'news'

urlpatterns = [
    path('probable-fights/', ProbableFightView.as_view(), name='probable-fights'),
]
