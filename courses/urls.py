from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    path('courses/<slug:slug>/edit', CourseUpdateView.as_view(), name='course-edit'),
    path('courses/create', CourseCreateView.as_view(), name='course-create'),
    path('courses/lessons/<int:pk>/edit', LessonUpdateView.as_view(), name='course-lesson-edit'),
    path('courses/<slug:slug>', CourseDetailView.as_view(), name='course-details'),
    path('courses/<slug:slug>/lessons', LessonsListView.as_view(), name='course-lessons'),
    path('courses/<slug:slug>/category', CoursesByCategoryListView.as_view(), name='course-by-category'),
]
