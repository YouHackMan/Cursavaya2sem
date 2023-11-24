from django.test import TestCase
from django.contrib.auth.models import User
from .models import Categories, Hashtag, Task, Filter, Notice
from django.utils import timezone

class CategoriesModelTest(TestCase):
    def test_name(self):
        category = Categories.objects.create(name="Test Category")
        self.assertEqual(str(category), "Test Category")

class HashtagModelTest(TestCase):
    def test_name(self):
        hashtag = Hashtag.objects.create(name="Test Hashtag")
        self.assertEqual(str(hashtag), "Test Hashtag")

class TaskModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        category = Categories.objects.create(name="Test Category")
        task = Task.objects.create(user=user, title="Test Task", category=category)

    def test_title(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.title, "Test Task")

    def test_complete_default_false(self):
        task = Task.objects.get(title="Test Task")
        self.assertFalse(task.complete)

    def test_date_default_now(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.date.strftime("%Y-%m-%d"), timezone.now().strftime("%Y-%m-%d"))

    def test_category(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(str(task.category), "Test Category")

class FilterModelTest(TestCase):
    def test_name(self):
        filter = Filter.objects.create(name="Test Filter")
        self.assertEqual(str(filter), "Test Filter")

class NoticeModelTest(TestCase):
    def test_notice(self):
        notice = Notice.objects.create(notice="Test Notice")
        self.assertEqual(str(notice), "Test Notice")