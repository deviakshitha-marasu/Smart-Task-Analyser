from django.urls import path
from tasks.views import analyze_tasks

urlpatterns = [
    path("tasks/analyze/", analyze_tasks, name="analyze_tasks"),
]
