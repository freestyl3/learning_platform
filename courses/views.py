from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Max
from .models import Course, Lesson, LessonImage
from .forms import CourseCreateForm, CourseForm, LessonForm

# Create your views here.

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'example.html'
    context_object_name = 'courses'

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'example.html'
    context_object_name = 'course'

class TeacherCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'teacher_example.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

class TeacherCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'teacher_example.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

@login_required
def create_course(request):
    if not request.user.is_teacher:
        messages.error(request, 'У вас нет прав для создания курсов')
        return redirect('homepage:home')
    
    if request.method == 'POST':
        form = CourseCreateForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Курс успешно создан')
            return redirect('courses:course_detail', pk=course.id)
    else:
        form = CourseCreateForm()
    
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def create_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Проверяем, является ли пользователь преподавателем курса
    if request.user != course.teacher:
        messages.error(request, 'У вас нет прав для создания уроков в этом курсе')
        return redirect('courses:course_detail', pk=course_id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            
            # Автоматически устанавливаем номер урока
            max_number = course.lesson_set.aggregate(Max('lesson_number'))['lesson_number__max']
            lesson.lesson_number = 1 if max_number is None else max_number + 1
            
            lesson.save()

            # Обработка загруженных изображений
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                LessonImage.objects.create(
                    lesson=lesson,
                    image=image,
                    order=i
                )
            
            messages.success(request, 'Урок успешно создан!')
            return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson.id)
    else:
        form = LessonForm()
    
    return render(request, 'courses/create_lesson.html', {'form': form, 'course': course})

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Получаем предыдущий и следующий уроки
    prev_lesson = Lesson.objects.filter(
        course=course,
        lesson_number__lt=lesson.lesson_number
    ).order_by('-lesson_number').first()
    
    next_lesson = Lesson.objects.filter(
        course=course,
        lesson_number__gt=lesson.lesson_number
    ).order_by('lesson_number').first()
    
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'course': course,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson
    })

@login_required
def edit_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Проверяем, является ли пользователь преподавателем курса
    if request.user != course.teacher:
        messages.error(request, 'У вас нет прав для редактирования уроков в этом курсе')
        return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            
            # Обработка загруженных изображений
            images = request.FILES.getlist('images')
            last_order = lesson.images.aggregate(Max('order'))['order__max'] or -1
            for i, image in enumerate(images, start=last_order + 1):
                LessonImage.objects.create(
                    lesson=lesson,
                    image=image,
                    order=i
                )
            
            messages.success(request, 'Урок успешно обновлен!')
            return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'courses/edit_lesson.html', {
        'form': form,
        'course': course,
        'lesson': lesson,
        'images': lesson.images.all()
    })

@login_required
def delete_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Проверяем, является ли пользователь преподавателем курса
    if request.user != course.teacher:
        messages.error(request, 'У вас нет прав для удаления уроков в этом курсе')
        return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    
    if request.method == 'POST':
        # Сохраняем номер удаляемого урока
        deleted_number = lesson.lesson_number
        
        # Удаляем урок
        lesson.delete()
        
        # Обновляем номера оставшихся уроков
        remaining_lessons = course.lesson_set.filter(lesson_number__gt=deleted_number)
        for remaining in remaining_lessons:
            remaining.lesson_number -= 1
            remaining.save()
        
        messages.success(request, 'Урок успешно удален')
        return redirect('courses:course_detail', pk=course_id)
    
    return render(request, 'courses/delete_lesson.html', {
        'course': course,
        'lesson': lesson
    })

@login_required
def delete_lesson_image(request, course_id, lesson_id, image_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    image = get_object_or_404(LessonImage, id=image_id, lesson=lesson)
    
    # Проверяем, является ли пользователь преподавателем курса
    if request.user != course.teacher:
        messages.error(request, 'У вас нет прав для удаления изображений')
        return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    
    image.delete()
    messages.success(request, 'Изображение успешно удалено')
    return redirect('courses:edit_lesson', course_id=course_id, lesson_id=lesson_id)
