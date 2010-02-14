import datetime

from django.contrib.auth.models import User
from django.db import models


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

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES,
                                default="a")
    created_on = models.DateTimeField(editable=False)
    closed_on = models.DateTimeField(editable=False, null=True, blank=True)
    assigned_to = models.ManyToManyField(User,
                                         limit_choices_to={"is_staff": True})
    reported_by = models.ForeignKey(User,
                                    related_name="reported_tasks")
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              default="open")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.datetime.now()
        
        if self.status == "closed":
            self.closed_on = datetime.datetime.now()

        super(Task, self).save(*args, **kwargs)
