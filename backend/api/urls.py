from django.urls import path
from .views import (
    RegisterView, LoginView, DatasetUploadView, DatasetListView, 
    RuleListCreateView, RuleDetailView, CheckRunView, CheckResultView,
    ReportDetailView, ReportTrendView
)

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('datasets/upload', DatasetUploadView.as_view(), name='upload_dataset'),
    path('datasets', DatasetListView.as_view(), name='list_datasets'),
    path('rules', RuleListCreateView.as_view(), name='list_create_rules'),
    path('rules/<int:pk>', RuleDetailView.as_view(), name='detail_rule'),
    path('checks/run/<int:pk>', CheckRunView.as_view(), name='run_checks'),
    path('checks/results/<int:pk>', CheckResultView.as_view(), name='check_results'),
    path('reports/trends', ReportTrendView.as_view(), name='report_trends'),
    path('reports/<int:pk>', ReportDetailView.as_view(), name='report_detail'),
]
