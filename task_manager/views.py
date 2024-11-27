from datetime import date
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)

from task_manager.forms import (
	TaskForm,
	WorkerCreateForm,
	WorkerUpdateForm,
	SearchForm,
)
from task_manager.models import Worker, Task


def index(request: HttpRequest) -> HttpResponse:
	return render(
		request, 'pages/index.html', {
			'total_tasks': Task.objects.count(),
			'active_tasks': Task.objects.filter(is_completed=False).count(),
			'total_users': get_user_model().objects.count(),
		}
	)


class SearchMixin:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["search_form"] = SearchForm(
			initial={
				"query": self.request.GET.get("query", "").strip()
			}
		)
		
		return context


class RedirectAuthenticatedUserLoginView(LoginView):
	"""Redirects authenticated users to the index page."""
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect("task_manager:index")
		return super().dispatch(request, *args, **kwargs)


class WorkerListView(SearchMixin, ListView):
	model = get_user_model()
	context_object_name = "worker_list"
	template_name = "pages/worker_list.html"
	paginate_by = 10
	
	def get_queryset(self):
		queryset = Worker.objects.select_related("position")
		
		search_query = self.request.GET.get("query", "").strip()
		if search_query:
			queryset = queryset.filter(
				Q(username__icontains=search_query) |
				Q(first_name__icontains=search_query) |
				Q(last_name__icontains=search_query)
			)
		
		return queryset


class WorkerDetailView(LoginRequiredMixin, DetailView):
	model = get_user_model()
	context_object_name = "worker"
	template_name = "pages/worker_detail.html"
	queryset = Worker.objects.select_related("position").prefetch_related(
		"tasks"
	)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context["active_tasks"] = self.object.tasks.filter(is_completed=False)
		context["resolved_tasks"] = self.object.tasks.filter(is_completed=True)
		context["today"] = date.today()
		
		return context


class WorkerCreateView(CreateView):
	model = get_user_model()
	form_class = WorkerCreateForm
	template_name = "pages/worker_form.html"
	
	def dispatch(self, request, *args, **kwargs):
		""" Redirects authenticated user to index page"""
		if request.user.is_authenticated:
			return redirect("task_manager:index")
		
		return super().dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse_lazy(
			"task_manager:worker_detail", kwargs={"pk": self.object.pk}
		)
	
	def form_valid(self, form):
		worker = form.save(commit=False)
		worker.set_password(form.cleaned_data["password"])
		worker.save()
		login(self.request, worker)
		
		return super().form_valid(form)


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
	model = get_user_model()
	form_class = WorkerUpdateForm
	template_name = "pages/worker_form.html"
	
	def dispatch(self, request, *args, **kwargs):
		worker = self.get_object()
		if not (request.user.is_superuser or request.user.pk == worker.pk):
			raise PermissionDenied(
				"You are not allowed to edit this user."
			)
		
		return super().dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		if next_url := self.request.GET.get('next'):
			return next_url
		
		return reverse_lazy(
			'task_manager:worker_detail', kwargs={'pk': self.get_object().pk}
		)
	
	def form_valid(self, form):
		worker = form.save(commit=False)
		
		if password := form.cleaned_data["password"]:
			worker.set_password(password)
			if worker.pk == self.request.user.pk:
				login(self.request, worker)
		else:
			del worker.password
		worker.save()
		
		return super().form_valid(form)


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
	model = get_user_model()
	template_name = "pages/worker_confirm_delete.html"
	success_url = reverse_lazy("task_manager:worker_list")
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			raise PermissionDenied(
				"You are not allowed to delete users."
			)
		
		return super().dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["previous_page"] = self.request.META.get("HTTP_REFERER", "/")
		
		return context


class TaskListView(SearchMixin, ListView):
	model = Task
	context_object_name = "task_list"
	template_name = "pages/task_list.html"
	paginate_by = 10
	
	def get_queryset(self):
		queryset = Task.objects.select_related("task_type").prefetch_related(
			"assignees"
		)
		
		search_query = self.request.GET.get("query", "").strip()
		if search_query:
			queryset = queryset.filter(name__icontains=search_query)
		
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
		
		context["today"] = date.today()
		context['is_coworker'] = (
			self.object.assignees.filter(pk=self.request.user.pk).exists()
		)
		
		return context


class TaskCreateView(LoginRequiredMixin, CreateView):
	model = Task
	form_class = TaskForm
	template_name = "pages/task_form.html"
	
	def get_success_url(self):
		return reverse_lazy(
			"task_manager:task_detail", kwargs={"pk": self.object.pk}
		)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
	model = Task
	form_class = TaskForm
	template_name = "pages/task_form.html"
	
	def dispatch(self, request, *args, **kwargs):
		task = self.get_object()
		is_user_assigner = task.assignees.filter(pk=request.user.pk).exists()
		
		if not (request.user.is_superuser or is_user_assigner):
			raise PermissionDenied(
				"You are not allowed to edit this task."
			)
		
		return super().dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		next_url = self.request.GET.get('next')
		if next_url:
			return next_url
		
		return reverse_lazy(
			'task_manager:worker_detail', kwargs={'pk': self.request.user.pk}
		)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
	model = Task
	template_name = "pages/task_confirm_delete.html"
	success_url = reverse_lazy("task_manager:task_list")
	
	def dispatch(self, request, *args, **kwargs):
		task = self.get_object()
		is_user_assigner = task.assignees.filter(pk=request.user.pk).exists()
		
		if not (request.user.is_superuser or is_user_assigner):
			raise PermissionDenied(
				"You are not allowed to delete this task."
			)
		
		return super().dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous_page'] = self.request.META.get('HTTP_REFERER', '/')
		
		return context
