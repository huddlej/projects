"""
Unit tests for the Projects application.
"""
import datetime

from django.test import TestCase

from forms import TasksForm
from models import Milestone, Project


class ProjectTestCase(TestCase):
    def test_get_current_milestone(self):
        today = datetime.date.today()
        project = Project.objects.create(name="Test")
        self.assertTrue(project.get_current_milestone() is None)

        milestone = Milestone.objects.create(
            project=project,
            start_date=today,
            end_date=(today + datetime.timedelta(days=1))
        )
        self.assertEqual(milestone, project.get_current_milestone())


class TasksFormTestCase(TestCase):
    def test_surrounding_whitespace(self):
        tasks_text = """
do this
do that
king of the castle
"""
        form = TasksForm({"tasks": tasks_text})
        self.assertTrue(form.is_valid())
        self.assertTrue(isinstance(form.cleaned_data["tasks"], list))
        self.assertTrue(len(form.cleaned_data["tasks"]) == 3)

    def test_no_whitespace(self):
        tasks_text = """do this
do that
king of the castle"""
        form = TasksForm({"tasks": tasks_text})
        self.assertTrue(form.is_valid())
        self.assertTrue(isinstance(form.cleaned_data["tasks"], list))
        self.assertTrue(len(form.cleaned_data["tasks"]) == 3)

    def test_no_content(self):
        tasks_text = ""
        form = TasksForm({"tasks": tasks_text})
        self.assertTrue(form.is_valid())
        self.assertTrue(isinstance(form.cleaned_data["tasks"], list))
        self.assertTrue(len(form.cleaned_data["tasks"]) == 0,
                        form.cleaned_data["tasks"])
