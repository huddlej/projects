from django import forms

from models import Milestone


class MilestoneForm(forms.ModelForm):
    class Meta:
        exclude = ("project",)
        model = Milestone
