from django import forms
from .models import *
  
class CourseForm(forms.ModelForm):
  
    class Meta:
        model = Course
        fields = ['title', 'category', 'short_description', 'description', 'outcome', 'requirements', 'language', 'level', 'thumbnail', 'price', 'video_url' ,'is_published' ]

    def save(self, commit=True):
        course = super(CourseForm, self).save(commit=False)
        if commit:
            course.save()
        return course

class LessonForm(forms.ModelForm):
  
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'duration', 'documents', 'handson_url']

    def save(self, commit=True):
        lesson = super(LessonForm, self).save(commit=False)
        if commit:
            lesson.save()
        return lesson