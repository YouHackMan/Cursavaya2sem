from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .api_views import ImportantTasksApiView
from .api_views import *
from .views import *
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoriesViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoriesViewSet, basename='category')

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'), 
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    #api_urls
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('categories/', CategoriesListCreateView.as_view(), name='categories-list-create'),
    path('categories/<int:pk>/', CategoriesDetailView.as_view(), name='categories-detail'),
    path('api/important-tasks/', ImportantTasksApiView.as_view(), name='important-tasks-api'),#2zadanie Q zapros 1 kod v api_views.py
    #zadanie8
    path('api/', include(router.urls)),
]