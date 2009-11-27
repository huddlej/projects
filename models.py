import datetime

from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """
    Represents a software project and all associated milestones.
    """        
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("projects_project", (self.id,))

    def get_current_milestone(self):
        today = datetime.date.today()
        milestones = self.milestone_set.filter(
            start_date__lte=today,
            end_date__gte=today
        )
        if milestones.count() > 0:
            return milestones[0]
        else:
            return None


class Milestone(models.Model):
    """
    Represents a set of tasks to be performed for a project by a certain date.
    """
    project = models.ForeignKey(Project)
    start_date = models.DateField(default=datetime.date.today())
    end_date = models.DateField()

    def __unicode__(self):
        return u"%s tasks for %s" % (self.project, self.end_date)

    @models.permalink
    def get_absolute_url(self):
        return ("projects_milestone", (self.project.id, self.id))


class Task(models.Model):
    """
    Represents a specific task to be completed for a specific milestone by one
    or more people.
    """
    STATUS_CHOICES = (("open", "Open"),
                      ("closed", "Closed"),
                      ("wontfix", "Won't Fix"),
                      ("duplicate", "Duplicate"))

    milestone = models.ForeignKey(Milestone)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    added_date = models.DateTimeField(editable=False)
    closed_date = models.DateTimeField(editable=False, null=True, blank=True)
    reported_by = models.ForeignKey(User,
                                    related_name="reported_tasks")
    assigned_to = models.ManyToManyField(User,
                                         limit_choices_to={"is_staff": True})
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              default="open")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("projects_task", (self.id,))

    def save(self, *args, **kwargs):
        if not self.id:
            self.added_date = datetime.datetime.now()
        
        if self.status == "closed":
            self.closed_date = datetime.datetime.now()

        super(Task, self).save(*args, **kwargs)
