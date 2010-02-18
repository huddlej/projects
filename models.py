import datetime

from django.contrib.auth.models import User
from django.db import models


class TaskQuerySet(models.query.QuerySet):
    def complete(self):
        for task in self:
            task.status = "closed"
            task.save()


class TaskManager(models.Manager):
    def get_query_set(self):
        return TaskQuerySet(self.model)        


class Task(models.Model):
    """
    Represents a specific task to be completed for a specific milestone by one
    or more people.
    """
    PRIORITY_CHOICES = (("a", "a"),
                        ("b", "b"),
                        ("c", "c"))
    STATUS_CHOICES = (("open", "Open"),
                      ("closed", "Closed"),
                      ("wontfix", "Won't Fix"),
                      ("duplicate", "Duplicate"))

    objects = TaskManager()

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES,
                                default="a")
    created_on = models.DateTimeField(editable=False)
    reported_by = models.ForeignKey(User,
                                    related_name="reported_tasks")
    assigned_to = models.ManyToManyField(User,
                                         limit_choices_to={"is_staff": True})
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              default="open")
    due_date = models.DateField(null=True, blank=True)
    closed_on = models.DateTimeField(editable=False, null=True, blank=True)

    class Meta:
        ordering = ("-priority", "due_date")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.datetime.now()
        
        if self.status == "closed":
            self.closed_on = datetime.datetime.now()

        super(Task, self).save(*args, **kwargs)
