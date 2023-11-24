from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from simple_history.models import HistoricalRecords #Отслеживание предыдущих версий объектов

class Categories(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    def __str__(self):
        return self.name

class Hashtag(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    def __str__(self):
        return self.name
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    filter = models.ForeignKey('Filter', on_delete=models.CASCADE, null = True)
    hashtag = models.ManyToManyField(Hashtag)
    notice = models.ForeignKey('Notice', on_delete=models.CASCADE, null = True)
    priority = models.ForeignKey('Priority', on_delete=models.CASCADE, null = True)
    history = HistoricalRecords()
    def __str__(self):
        return "{0} — {1}".format(self.title, self.date)
class Meta:
        order_with_respect_to = 'user'

    
class Filter(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    def __str__(self):
        return self.name
class Notice(models.Model):
    notice= models.CharField(max_length=200)
    def __str__(self):
        return self.notice
class Priority(models.Model):
    priority=models.CharField(max_length=200)
    def __str__(self):
        return self.priority