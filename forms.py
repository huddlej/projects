from django import forms

from models import Milestone


class MilestoneForm(forms.ModelForm):
    class Meta:
        exclude = ("project",)
        model = Milestone


class TasksForm(forms.Form):
    """
    Processes a text field as a list of tasks separated by line returns.
    """
    tasks = forms.CharField(widget=forms.Textarea(), required=False)

    def clean_tasks(self):
        """
        Breaks a paragraph of tasks separated by line returns into a list of
        tasks.
        """
        return [task 
                for task in self.cleaned_data["tasks"].strip().split("\n")
                if task]
