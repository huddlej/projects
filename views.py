"""
Views for Projects application.
"""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import AddTaskForm, EditTaskForm
from models import Task


@login_required
def index(request):
    post_data = request.POST or None

    if request.GET.get("status") == "completed":
        tasks = Task.objects.completed()
    else:
        tasks = Task.objects.open()

    others_tasks = tasks.exclude(assigned_to=request.user)
    tasks = tasks.filter(assigned_to=request.user)    

    # Handle multiple task updates (e.g. deletes, completes, etc.).
    if post_data and "task" in post_data:
        task_ids = post_data.getlist("task")
        tasks = Task.objects.filter(pk__in=task_ids)

        if "delete" in post_data:
            tasks.delete()
            return HttpResponseRedirect(reverse("projects_index"))
        elif "mark_complete" in post_data:
            tasks.complete()
            return HttpResponseRedirect(reverse("projects_index"))

    form = AddTaskForm(post_data)
    if form.is_valid():
        task = form.save(commit=False)
        task.reported_by = request.user
        task.save()
        task.assigned_to.add(request.user)
        
        return HttpResponseRedirect(reverse("projects_index"))        

    for task in tasks:
        task.form = EditTaskForm(post_data, instance=task, prefix=task.id)
        if task.form.is_valid():
            task = task.form.save()
    
    context = {"page_title": "Projects",
               "tasks": tasks,
               "others_tasks": others_tasks,
               "form": form}
    return render_to_response("projects/index.html", context,
                              context_instance=RequestContext(request))
