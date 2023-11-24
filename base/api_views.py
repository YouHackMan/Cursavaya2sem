from rest_framework import generics, pagination
from django.db.models import Q
from .models import Task, Categories
from .serializers import TaskSerializer, CategoriesSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CategoriesListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class CategoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class ImportantTasksApiView(generics.ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        keyword = self.request.GET.get('keyword', 'Корм на столе')
        category_name = self.request.GET.get('category_name', 'Домашние животные')
        complete = self.request.GET.get('complete', 'false')

        queryset = Task.objects.all()

        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))

        if category_name:
            queryset = queryset.filter(category__name=category_name)

        if complete is not None:
            queryset = queryset.filter(complete=complete.lower() == 'true')

        return queryset
#class ImportantTasksApiView(APIView):
    #permission_classes = []  # Убирает DjangoModelPermissionsOrAnonReadOnly
    #def get(self, request, format=None):
        #queryset = Task.objects.all()
        #serializer = TaskSerializer(queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)