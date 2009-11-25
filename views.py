"""
Views for Projects application.
"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list

from forms import MilestoneForm
from models import Project


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
    """Represents interactions with a single project."""
    project = Project.objects.get(pk=object_id)

    if request.method == "POST":
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            return HttpResponseRedirect(milestone.get_absolute_url())
    else:
        form = MilestoneForm()

    context = {"form": form,
               "object": project}
    return render_to_response("projects/project_detail.html", context)
