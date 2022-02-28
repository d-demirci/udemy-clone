from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from cart.cart import Cart
from courses.forms import CourseForm, LessonForm
from courses.models import Course, Category, Lesson
from lms.models import Enroll


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)
        else:
            cart = Cart(self.request)
            context['is_in_cart'] = cart.has_course(course)
        return context


class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context

class CourseCreateView(CreateView):
    # fields = ['title', 'category', 'short_description', 'description', 'outcome', 'requirements', 'language', 'level', 'thumbnail', 'video_url' ,'is_published' ]
    model = Course
    template_name = 'courses/course_form.html'
    success_url = '/login'
    form_class = CourseForm 

    extra_context = {
        'title': 'Kurs Oluştur'
    }

    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return super().dispatch(self.request, *args, **kwargs)
    #     return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return self.success_url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        course_form = self.form_class(data=request.POST, files=request.FILES)
        self.object = course_form.save(commit=False)
        self.object.user = self.request.user
        if self.form_valid(course_form):
            course = course_form.save()
            course_form.save_m2m()
            return redirect('courses:edit', pk=course.id)
        else:
            return render(request, 'courses/course_form.html', {'form': course_form})


class CourseUpdateView(UpdateView):
    # fields = ['title', 'category', 'short_description', 'description', 'outcome', 'requirements', 'language', 'level', 'thumbnail', 'video_url' ,'is_published' ]
    model = Course
    template_name = 'courses/course_form.html'
    success_url = '/login'
    form_class = CourseForm 

    extra_context = {
        'title': 'Kurs Oluştur'
    }

    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return super().dispatch(self.request, *args, **kwargs)
    #     return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return self.success_url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        course_form = self.form_class(data=request.POST, files=request.FILES)
        self.object = course_form.save(commit=False)
        self.object.user = self.request.user
        if self.form_valid(course_form):
            course = course_form.save()
            course_form.save_m2m()
            return redirect('courses:edit', pk=course.id)
        else:
            return render(request, 'courses/course_form.html', {'form': course_form})


class LessonsListView(ListView):
    model = Lesson
    template_name = 'lessons/lessons_list_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        return context

class LessonUpdateView(UpdateView):
    # fields = ['title', 'category', 'short_description', 'description', 'outcome', 'requirements', 'language', 'level', 'thumbnail', 'video_url' ,'is_published' ]
    model = Lesson
    template_name = 'lessons/lesson_form.html'
    success_url = '/login'
    form_class = LessonForm 
    extra_context = {
        'title': 'Dersi Düzenle'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        course = Course.objects.get(slug=lesson.course.slug)
        context['course'] = course
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return super().dispatch(self.request, *args, **kwargs)
    #     return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return self.success_url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        return super(LessonUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        lesson_form = self.form_class(data=request.POST, files=request.FILES, instance=lesson)
        if self.form_valid(lesson_form):
            lesson_form.save()
            lesson_form.save_m2m()
            return redirect('courses:course-lesson-edit', pk=lesson.id)
        else:
            return render(request, 'lessons/lesson_form.html', {'form': lesson_form})
