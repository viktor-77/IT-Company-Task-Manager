from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import (
	ListView,
	DetailView,
	# CreateView,
	# DeleteView,
)

from task_manager.models import Task
from task_manager.models import Worker


def index(request):
	total_tasks = Task.objects.count()
	active_tasks = Task.objects.filter(
		is_completed=False
	).count()
	total_users = get_user_model().objects.count()
	last_tasks = Task.objects.all().order_by('-id')[:3]
	return render(
		request, 'pages/index.html', {
			'total_tasks': total_tasks,
			'active_tasks': active_tasks,
			'total_users': total_users,
			"last_tasks": last_tasks,
		}
	)


class WorkerListView(ListView):
	model = Worker
	context_object_name = "worker_list"
	template_name = "pages/worker_list.html"
	paginate_by = 2
	
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


class WorkerDetailView(DetailView):
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
