from django.contrib import admin
#zadanie6 
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Task, Categories, Hashtag, Filter, Notice, Priority

class TaskResource(resources.ModelResource):
    class Meta:
        model = Task

class TaskAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'complete', 'date', 'category', 'filter')
    list_filter = ('user', 'category', 'date')
    date_hierarchy = 'date'
    filter_horizontal = ('hashtag',)
    search_fields = ('title',)
    ordering = ('-user',)
    resource_class = TaskResource  # Используем созданный ресурс для экспорта

admin.site.register(Task, TaskAdmin)
admin.site.register(Categories)
admin.site.register(Hashtag)
admin.site.register(Filter)
admin.site.register(Notice)
admin.site.register(Priority)