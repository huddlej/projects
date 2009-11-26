from django.conf.urls.defaults import patterns, url
from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_detail

from models import Milestone, Project, Task
from views import milestone_detail, project_detail, projects


urlpatterns = patterns("",
    url(r"^$", projects, name="projects_index"),

    url(r"^project/(?P<object_id>\d+)/$", project_detail,
        name="projects_project"),

    url(r"^project/add/$", create_object,
        {"model": Project},
        name="projects_project_add"),

    url(r"^project/(?P<project_id>\d+)/milestone/(?P<object_id>\d+)/$",
        milestone_detail,
        name="projects_milestone"),

    url(r"^project/(?P<project_id>\d+)/milestone/add/$", milestone_detail,
        name="projects_milestone_create"),

    url(r"^task/(?P<object_id>\d+)/$", update_object,
        {"model": Task},
        name="projects_task"),

    url(r"^task/add/$", create_object,
        {"model": Task},
        name="projects_task_add"),
)
