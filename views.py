"""
Views for Projects application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import TaskForm
from models import Task


@login_required
def index(request):
    tasks = Task.objects.all()
    post_data = request.POST or None
    form = TaskForm(post_data)

    if form.is_valid():
        task = form.save(commit=False)
        task.reported_by = request.user
        task.save()
        task.assigned_to.add(request.user)
        task.save_m2m()
        form = TaskForm()
    
    context = {"page_title": "Projects",
               "tasks": tasks,
               "form": form}
    return render_to_response("projects/index.html", context,
                              context_instance=RequestContext(request))
