from django import forms
from django.contrib.auth.models import User

from models import Task


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name",)


class EditTaskForm(forms.ModelForm):
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES,
                                 widget=forms.RadioSelect(),
                                 required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "cols": 30}),
        required=False
    )
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    user = forms.CharField(max_length=12,
                           required=False,
                           widget=forms.TextInput(attrs={"size": 9}))
    
    class Meta:
        model = Task
        fields = ("priority", "description", "assigned_to")

    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.assigned_to.count() > 0:
            self.fields["assigned_to"].choices = [(u.id, u.get_full_name())
                                                  for u in self.instance.assigned_to.all()]

    def clean_user(self):
        user = self.cleaned_data["user"]
        if user:
            try:
                user = User.objects.get(username=self.cleaned_data["user"])
            except User.DoesNotExist, e:
                raise forms.ValidationError(e.message)

        return user


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
