from django.urls import path, re_path

from .views import ProbableFightView, ApproveFightRecordView

app_name = 'news'

urlpatterns = [
    path('probable-fights/', ProbableFightView.as_view(), name='probable-fights'),
    path('fights/<int:pk>/approve/', ApproveFightRecordView.as_view(), name='fight-record-approve'),
]
