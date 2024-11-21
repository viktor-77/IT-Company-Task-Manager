from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
	View,
	ListView,
	DetailView,
	CreateView,
	DeleteView,
)
from django.views.generic import UpdateView

from task_manager.forms import TaskForm
from task_manager.models import Task
from task_manager.models import Worker


def index(request):
	total_tasks = Task.objects.count()
	active_tasks = Task.objects.filter(
		is_completed=False
	).count()
	total_users = get_user_model().objects.count()
	return render(
		request, 'pages/index.html', {
			'total_tasks': total_tasks,
			'active_tasks': active_tasks,
			'total_users': total_users,
		}
	)


class CustomLoginView(LoginView):
	"""Prevents authenticated users get login page"""
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect("task_manager:index")
		return super().dispatch(request, *args, **kwargs)


class WorkerListView(ListView):
	model = Worker
	context_object_name = "worker_list"
	template_name = "pages/worker_list.html"
	paginate_by = 10
	
	def get_queryset(self):
		queryset = Worker.objects.select_related("position")
		search_query = self.request.GET.get("search")
		
		if search_query:
			queryset = queryset.filter(
				Q(username__icontains=search_query) |
				Q(first_name__icontains=search_query) |
				Q(last_name__icontains=search_query)
			)
		return queryset


class WorkerDetailView(LoginRequiredMixin, DetailView):
	model = Worker
	context_object_name = "worker"
	template_name = "pages/worker_detail.html"
	queryset = Worker.objects.select_related("position").prefetch_related(
		"tasks"
	)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["tasks"] = self.object.tasks.all()
		context["total_tasks"] = self.object.tasks.count()
		context["today"] = date.today()
		context["active_tasks"] = self.object.tasks.filter(
			is_completed=False
		).count()
		
		return context


class TaskListView(ListView):
	model = Task
	context_object_name = "task_list"
	template_name = "pages/task_list.html"
	paginate_by = 10
	
	def get_queryset(self):
		queryset = Task.objects.select_related("task_type").prefetch_related(
			"assignees"
		)
		search_query = self.request.GET.get("search")
		if search_query:
			queryset = queryset.filter(Q(name__icontains=search_query))
		
		return queryset


class TaskDetailView(LoginRequiredMixin, DetailView):
	model = Task
	context_object_name = "task"
	template_name = "pages/task_detail.html"
	queryset = Task.objects.select_related("task_type").prefetch_related(
		"assignees"
	)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['is_coworker'] = (
			self.object.assignees.filter(pk=self.request.user.pk).exists()
		)
		return context


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Task
	form_class = TaskForm
	template_name = "pages/task_form.html"
	
	def get_success_url(self):
		return reverse_lazy(
			"task_manager:task_detail", kwargs={"pk": self.object.pk}
		)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Task
	form_class = TaskForm
	template_name = "pages/task_form.html"
	success_url = reverse_lazy("task_manager:task_list")
	
	def get_success_url(self):
		next_url = self.request.GET.get('next')
		if next_url:
			return next_url
		return reverse_lazy(
			'task_manager:worker_detail', kwargs={'pk': self.request.user.pk}
		)


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Task
	template_name = "pages/confirm_delete.html"
	success_url = reverse_lazy("task_manager:task_list")
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous_page'] = self.request.META.get('HTTP_REFERER', '/')
		return context
