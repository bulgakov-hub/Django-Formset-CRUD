from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import TestBox, QuestionTest, AnswerQuestion


class TestBoxForm(forms.ModelForm):
    """Форма теста"""

    class Meta:
        model = TestBox
        fields = '__all__'


class QuestionTestForm(forms.ModelForm):
    """Форма вопросов теста"""

    class Meta:
        model = QuestionTest
        fields = ['question']


class AnswerQuestionForm(forms.ModelForm):
    """Форма вариантов ответа"""

    class Meta:
        model = AnswerQuestion
        fields = ['prefix_name', 'right']


# Формсет ответов на вопросы
AnswerQuestionFormset = inlineformset_factory(
    QuestionTest, AnswerQuestion, form=AnswerQuestionForm, widgets={
        'prefix_name': forms.HiddenInput(), 'right': forms.CheckboxInput()},
    fields=['prefix_name', 'right'], extra=4, can_delete=False)


# Обертка формсета ответов на вопросы
def getAnswerQuestionFormset(extra=4):
    AnswerQuestionFormset.extra = extra
    return AnswerQuestionFormset


class BaseFormset(BaseInlineFormSet):
    """Формсет вопросов с вложенным формсетом ответов"""

    _data = {}

    def add_fields(self, form, index):

        super().add_fields(form, index)
        data = self._data

        if data:
            initial_process = data[index]['data']
            extra = int(data[index]['nested_extra'])
        else:
            initial_process = None
            extra = None

        form.nested = getAnswerQuestionFormset(extra)(
            initial=initial_process,
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='answer-%s-%s' % (
                form.prefix,
                AnswerQuestionFormset.get_default_prefix()
            )
        )

    def is_valid(self):
        result = super().is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):
        result = super().save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'nested'):
                form.nested.save(commit=commit)

        return result

    @classmethod
    def set_data(cls, data):
        cls._data = data


def getTestFormset(extra=14, data={}):
    """Обертка формсета вопросов (extra - кол-во форм для вопросов,
    data = [{'nested_extras': int, 'data': [{'prefix_name': 'А'}, ...]
    nested_extras - кол-во форм ответов
    data - набор префиксов ответов А, Б, В, Г)
    """

    BaseFormset.set_data(data)
    return inlineformset_factory(
        TestBox,
        QuestionTest,
        formset=BaseFormset,
        widgets={
            'question': forms.TextInput(
                attrs={
                    'class': 'question-input text-center disabled',
                    'readonly': 'readonly',
                    'style': ''})},
        fields=[
            'question',
        ],
        extra=extra,
        can_delete=False)
