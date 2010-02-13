"""
Views for Projects application.
"""
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list

from forms import MilestoneForm, TasksForm
from models import Milestone, Project


class JsonResponse(HttpResponse):
    """Represents a Django response containing JSON data."""
    def __init__(self, data):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(data),
            mimetype="application/json"
        )


def validate_form(request, form_class):
    """Validates a given form class when posted to by an AJAX call."""
    form = form_class(request.POST)
    if request.GET.has_key("field"):
        errors = form.errors.get(request.GET["field"], [])
    else:
        errors = form.errors

    return JsonResponse({
        "valid": not errors,
        "errors": errors
    })


def projects(request):
    """Represents a list of all projects."""
    form_response = create_object(request, model=Project)
    if not form_response.content:
        return form_response

    extra_context = {"form": form_response.content}
    return object_list(request, Project.objects.all(),
                       extra_context=extra_context)


def project_detail(request, object_id):
    """
    Redirects users to either the current milestone for this project or the form
    to add a new milestone.
    """
    project = get_object_or_404(Project, pk=object_id)
    current_milestone = project.get_current_milestone()

    if current_milestone:
        return HttpResponseRedirect(current_milestone.get_absolute_url())
    else:
        return HttpResponseRedirect(reverse("projects_milestone_create",
                                            args=(project.id,)))


def milestone_detail(request, project_id, object_id=None):
    """
    Describes a milestone for a given project or a form to create a new
    milestone for that same project.
    """
    project = get_object_or_404(Project, pk=project_id)

    if object_id is None:
        milestone = None
        form_args = {}
    else:
        milestone = get_object_or_404(Milestone, pk=object_id)
        form_args = {"instance": milestone}

    if request.method == "POST":
        form = MilestoneForm(request.POST, **form_args)
        tasks_form = TasksForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            return HttpResponseRedirect(milestone.get_absolute_url())
    else:
        form = MilestoneForm(**form_args)
        tasks_form = TasksForm()

    context = {"form": form,
               "tasks_form": tasks_form,
               "project": project}
    return render_to_response("projects/milestone_form.html", context)
