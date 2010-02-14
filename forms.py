from django import forms

from models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name",)


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
