from django.contrib import admin
from django.urls import path

from task_manager.views import index, WorkerListView, WorkerDetailView

urlpatterns = [
	path("", index, name="index"),
	path("workers/", WorkerListView.as_view(), name="worker_list"),
	path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"),
]

app_name = "task_manager"
