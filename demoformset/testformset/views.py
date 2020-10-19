from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import TestBox, QuestionTest
from .forms import TestBoxForm
from .services import TestManagerFormset
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST


# Функция для сортировки по номеру вопроса
def key_sort(arg):

    number = arg.question
    if number.isdigit():
        result = int(number)
    else:
        result = number
    return result


# Ответы на тест (модальное окно)
@require_POST
def get_answers(request):

    testbox_id = request.POST.get('testbox_id')
    qs = QuestionTest.objects.filter(test_box=testbox_id)
    # Функция сортировки по номеру вопроса
    questions = sorted(qs, key=key_sort)
    data = {'question': questions}

    return render(request, 'testformset/modal_answers_list.html', data)


class TestListView(ListView):
    """Список тестов"""

    model = TestBox
    template_name = 'testformset/test_list.html'
    paginate_by = 5
    context_object_name = 'test_list'


class TestCreateView(CreateView):
    """Создание теста"""

    model = TestBox
    template_name = 'testformset/test_operation.html'

    success_url = reverse_lazy('testformset:list')
    success_message = "Тест успешно добавлен в список"
    error_message = "Возникла ошибка"
    fields = '__all__'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        manager_formset = TestManagerFormset()

        if self.request.POST:
            context['question_set'] = manager_formset.post(
                self.request.POST)
        else:

            context['question_set'] = manager_formset.create()
            context['answers_prefix'] = manager_formset.data.set.answers
            context['title'] = 'Добавить тест'

        return context

    def form_valid(self, form):

        context = self.get_context_data(form=form)
        question_set = context['question_set']

        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        quantity_q = form.cleaned_data['quantity_q']
        quantity_a = form.cleaned_data['quantity_a']

        self.object = form.save(commit=False)
        self.object.name = name
        self.object.description = description
        self.object.quantity_q = quantity_q
        self.object.quantity_a = quantity_a

        if question_set.is_valid():
            self.object.save()
            question_set.instance = self.object
            question_set.save()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                self.success_message)
            return redirect('testformset:list')

        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                self.error_message)
            return redirect('testformset:list')


# Изменить параметры формсета
@require_POST
def get_formset(request):

    q = int(request.POST.get('q'))
    a = int(request.POST.get('a'))

    manager_formset = TestManagerFormset(q, a)
    question_set = manager_formset.create()
    answers_prefix = manager_formset.data.set.answers

    data = {'question_set': question_set, 'answers_prefix': answers_prefix}

    return render(request, 'testformset/test_answer_input.html', data)


class TestUpdateView(UpdateView):
    """Изменить тест"""

    model = TestBox
    template_name = 'testformset/test_operation.html'
    form = TestBoxForm
    success_url = reverse_lazy('testformset:list')
    success_message = "Тест успешно изменен"
    error_message = "Возникла ошибка"
    fields = '__all__'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        manager_formset = TestManagerFormset(
            self.object.quantity_q, self.object.quantity_a)
        if self.request.POST:
            context['question_set'] = manager_formset.post(
                self.request.POST, instance=self.object)
        else:
            context['question_set'] = manager_formset.update(
                instance=self.object)
            context['answers_prefix'] = manager_formset.data.set.answers
            context['title'] = 'Изменить тест'

        return context

    def form_valid(self, form):

        context = self.get_context_data(form=form)
        question_set = context['question_set']
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        quantity_q = form.cleaned_data['quantity_q']
        quantity_a = form.cleaned_data['quantity_a']

        self.object = form.save(commit=False)
        self.object.name = name
        self.object.description = description
        self.object.quantity_q = quantity_q
        self.object.quantity_a = quantity_a

        if question_set.is_valid():
            self.object.save()
            question_set.instance = self.object
            question_set.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                self.success_message)
            return redirect('testformset:list')

        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                self.error_message)
            return redirect('testformset:list')


class TestDeleteView(DeleteView):
    """Удалить тест"""

    model = TestBox
    success_url = reverse_lazy('testformset:list')
    success_message = "Тест успешно удален"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TestDeleteView, self).delete(request, *args, **kwargs)
