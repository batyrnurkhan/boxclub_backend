from django.urls import path, re_path

from profiles.views import UnapprovedFightRecordListView
from .views import ProbableFightView, ApproveFightRecordView

app_name = 'news'

urlpatterns = [
    path('probable-fights/', ProbableFightView.as_view(), name='probable-fights'),
    path('fights/<int:pk>/approve/', ApproveFightRecordView.as_view(), name='fight-record-approve'),
    path('fights/<int:id>/unapproved/', UnapprovedFightRecordListView.as_view(), name='unapproved-fight-records'),
    path('fights/probable/<int:id>/', ProbableFightView.as_view(), name='probable-fight-detail'),

]
