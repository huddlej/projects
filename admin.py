from django.contrib import admin

from models import Milestone, Project, Task


class TaskInline(admin.StackedInline):
    model = Task


class MilestoneAdmin(admin.ModelAdmin):
    inlines = [TaskInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save(reported_by=request.user)

        formset.save_m2m()


class MilestoneInline(admin.TabularInline):
    model = Milestone


class ProjectAdmin(admin.ModelAdmin):
    inlines = [MilestoneInline]


admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task)
