"""
Unit tests for the Projects application.
"""
import datetime

from django.test import TestCase

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
                                             
