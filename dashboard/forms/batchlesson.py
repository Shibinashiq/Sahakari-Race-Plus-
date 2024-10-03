
from django import forms
from dashboard.views.imports import *
class BatchLessonForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_deleted=False), required=True)

    class Meta:
        model = BatchLesson
        fields = ['lesson', 'visible_in_days'] 