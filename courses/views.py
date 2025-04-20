from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Max
from .models import Course, Lesson, LessonImage, Test, Question, ChoiceQuestion, TestResult
from .forms import CourseCreateForm, CourseForm, LessonForm, TestForm, QuestionForm, InputQuestionForm
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your views here.

class TestListView(LoginRequiredMixin, ListView):
    model = TestResult
    template_name = 'courses/test_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return TestResult.objects.filter(test_id=test_id)

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'example.html'
    context_object_name = 'courses'

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class TeacherCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'teacher_example.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

class TeacherCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/teacher_dashboard.html'
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
    if not request.user.is_teacher:
        return JsonResponse({'error': 'Только преподаватели могут создавать уроки'}, status=403)

    course = get_object_or_404(Course, id=course_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        
        if form.is_valid():
            try:
                lesson = form.save(commit=False)
                lesson.course = course
                
                # Get the highest lesson number for this course
                highest_lesson = Lesson.objects.filter(course=course).order_by('-lesson_number').first()
                lesson.lesson_number = (highest_lesson.lesson_number + 1) if highest_lesson else 1
                
                lesson.save()

                # Обработка загруженных изображений
                images = request.FILES.getlist('images')
                image_positions = {}
                
                try:
                    image_positions = request.POST.get('image_positions', '{}')
                    import json
                    image_positions = json.loads(image_positions)
                except json.JSONDecodeError:
                    image_positions = {}

                # Сохраняем изображения и их подписи
                for i, image in enumerate(images):
                    image_id = f'image-{i}'
                    caption = image_positions.get(image_id, '')
                    
                    LessonImage.objects.create(
                        lesson=lesson,
                        image=image,
                        caption=caption,
                        order=i
                    )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Урок успешно создан',
                        'redirect_url': reverse('courses:course_detail', args=[course.id])
                    })
                return redirect('courses:course_detail', course_id=course.id)
                
            except Exception as e:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=400)
                messages.error(request, f'Ошибка при создании урока: {str(e)}')
        else:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = LessonForm()
        if is_ajax:
            return JsonResponse({
                'success': False,
                'error': 'GET-запросы не поддерживаются для AJAX'
            }, status=405)
    
    context = {
        'form': form,
        'course': course
    }
    return render(request, 'courses/create_lesson.html', context)

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
    
    # Получаем тест для урока, если он есть
    test = Test.objects.filter(lesson=lesson).first()
    test_result = None
    
    # Если есть тест и пользователь не преподаватель, получаем результат теста
    if test and request.user != course.teacher:
        test_result = TestResult.objects.filter(
            user=request.user,
            test=test
        ).first()
    
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'course': course,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'test': test,
        'test_result': test_result
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
        try:
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
        except Exception as e:
            messages.error(request, f'Ошибка при удалении урока: {str(e)}')
            return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    
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

@login_required
def create_test(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.lesson = lesson
            test.save()
            messages.success(request, 'Тест успешно создан')
            return redirect('courses:edit_test', course_id=course_id, lesson_id=lesson_id, test_id=test.id)
    else:
        test_form = TestForm()
    
    return render(request, 'courses/create_test.html', {
        'form': test_form,
        'course': course,
        'lesson': lesson
    })

@login_required
def edit_test(request, course_id, lesson_id, test_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    test = get_object_or_404(Test, id=test_id, lesson=lesson)
    
    if request.method == 'POST':
        test_form = TestForm(request.POST, instance=test)
        if test_form.is_valid():
            test_form.save()
            messages.success(request, 'Тест успешно обновлен')
            return redirect('courses:course_detail', pk=course_id)
    else:
        test_form = TestForm(instance=test)
    
    questions = Question.objects.filter(test_id=test)
    
    return render(request, 'courses/edit_test.html', {
        'form': test_form,
        'course': course,
        'lesson': lesson,
        'test': test,
        'questions': questions
    })

@login_required
def add_question(request, course_id, lesson_id, test_id):
    try:
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
        test = get_object_or_404(Test, id=test_id, lesson=lesson)
        
        if request.method == 'POST':
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            question_form = QuestionForm(request.POST)
            input_form = InputQuestionForm(request.POST)
            
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.test_id = test
                question.save()
                
                if question.type == 'input':
                    if input_form.is_valid():
                        input_question = input_form.save(commit=False)
                        input_question.question = question
                        input_question.save()
                        if is_ajax:
                            return JsonResponse({
                                'success': True,
                                'message': 'Вопрос успешно добавлен',
                                'redirect': reverse('courses:edit_test', args=[course_id, lesson_id, test_id])
                            })
                        messages.success(request, 'Вопрос успешно добавлен')
                        return redirect('courses:edit_test', course_id=course_id, lesson_id=lesson_id, test_id=test_id)
                    else:
                        question.delete()
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'errors': input_form.errors
                            }, status=400)
                        messages.error(request, 'Пожалуйста, введите правильный ответ')
                        return render(request, 'courses/add_question.html', {
                            'question_form': question_form,
                            'input_form': input_form,
                            'course': course,
                            'lesson': lesson,
                            'test': test
                        })
                
                elif question.type == 'multiple_choice':
                    # Собираем все варианты ответов из формы
                    choices = []
                    choice_texts = request.POST.getlist('choice_text[]', [])
                    is_correct_list = request.POST.getlist('is_correct[]', [])
                    
                    for i, choice_text in enumerate(choice_texts):
                        if choice_text.strip():
                            is_correct = str(i) in is_correct_list
                            choices.append({
                                'text': choice_text.strip(),
                                'is_correct': is_correct
                            })
                    
                    if not choices:
                        question.delete()
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'errors': {'choices': ['Добавьте хотя бы один вариант ответа']}
                            }, status=400)
                        messages.error(request, 'Добавьте хотя бы один вариант ответа')
                        return render(request, 'courses/add_question.html', {
                            'question_form': question_form,
                            'input_form': input_form,
                            'course': course,
                            'lesson': lesson,
                            'test': test
                        })
                    else:
                        # Проверяем, есть ли хотя бы один правильный ответ
                        has_correct = any(choice['is_correct'] for choice in choices)
                        if not has_correct:
                            question.delete()
                            if is_ajax:
                                return JsonResponse({
                                    'success': False,
                                    'errors': {'choices': ['Выберите хотя бы один правильный ответ']}
                                }, status=400)
                            messages.error(request, 'Выберите хотя бы один правильный ответ')
                            return render(request, 'courses/add_question.html', {
                                'question_form': question_form,
                                'input_form': input_form,
                                'course': course,
                                'lesson': lesson,
                                'test': test
                            })
                        
                        # Сохраняем варианты ответов
                        for choice in choices:
                            ChoiceQuestion.objects.create(
                                question_id=question,
                                text=choice['text'],
                                is_correct=choice['is_correct']
                            )
                        
                        if is_ajax:
                            return JsonResponse({
                                'success': True,
                                'message': 'Вопрос успешно добавлен',
                                'redirect': reverse('courses:edit_test', args=[course_id, lesson_id, test_id])
                            })
                        messages.success(request, 'Вопрос успешно добавлен')
                        return redirect('courses:edit_test', course_id=course_id, lesson_id=lesson_id, test_id=test_id)
            else:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'errors': question_form.errors
                    }, status=400)
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
                return render(request, 'courses/add_question.html', {
                    'question_form': question_form,
                    'input_form': input_form,
                    'course': course,
                    'lesson': lesson,
                    'test': test
                })
        else:
            question_form = QuestionForm()
            input_form = InputQuestionForm()
        
        return render(request, 'courses/add_question.html', {
            'question_form': question_form,
            'input_form': input_form,
            'course': course,
            'lesson': lesson,
            'test': test
        })
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': {'__all__': [str(e)]}
            }, status=500)
        raise

@login_required
def take_test(request, course_id, lesson_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    test = get_object_or_404(Test, id=test_id, lesson=lesson)
    
    # Проверяем, что пользователь не преподаватель этого курса
    if request.user == course.teacher:
        messages.error(request, 'Преподаватель не может проходить тест')
        return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    
    if request.method == 'POST':
        # Получаем все вопросы теста
        questions = Question.objects.filter(test_id=test)
        correct_answers = 0
        total_questions = questions.count()
        
        for question in questions:
            if question.type == 'input':
                # Для вопросов с текстовым вводом
                user_answer = request.POST.get(f'answer_{question.id}', '').strip()
                correct_answer = question.inputquestion.right_answer
                if user_answer.lower() == correct_answer.lower():
                    correct_answers += 1
            else:
                # Для вопросов с множественным выбором
                correct_choices = set(question.choicequestion_set.filter(is_correct=True).values_list('id', flat=True))
                user_choices = set(map(int, request.POST.getlist(f'answer_{question.id}', [])))
                if correct_choices == user_choices:
                    correct_answers += 1
        
        # Вычисляем процент правильных ответов
        if total_questions > 0:
            score_percentage = (correct_answers / total_questions) * 100
        else:
            score_percentage = 0
        
        # Сохраняем результат теста
        TestResult.objects.create(
            user=request.user,
            test=test,
            score=score_percentage,
            completed_at=timezone.now()
        )
        
        messages.success(
            request, 
            f'Тест завершен! Правильных ответов: {correct_answers} из {total_questions} ({score_percentage:.1f}%)'
        )
        return redirect('courses:lesson_detail', course_id=course_id, lesson_id=lesson_id)
    
    # Получаем вопросы для теста
    questions = Question.objects.filter(test_id=test).prefetch_related(
        'choicequestion_set',
        'inputquestion'
    )
    
    return render(request, 'courses/take_test.html', {
        'course': course,
        'lesson': lesson,
        'test': test,
        'questions': questions
    })

@login_required
def delete_question(request, course_id, lesson_id, test_id, question_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    test = get_object_or_404(Test, id=test_id, lesson=lesson)
    question = get_object_or_404(Question, id=question_id, test_id=test)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Вопрос успешно удален')
        return redirect('courses:edit_test', course_id=course_id, lesson_id=lesson_id, test_id=test_id)
    
    return render(request, 'courses/delete_question.html', {
        'course': course,
        'lesson': lesson,
        'test': test,
        'question': question
    })

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс успешно удален')
        return redirect('courses:teacher_course_list')
    
    return render(request, 'courses/delete_course.html', {
        'course': course
    })
