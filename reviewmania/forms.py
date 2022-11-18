from django import forms
from django.forms import formset_factory
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReviewScoreForm(forms.Form):
    criteria_name = forms.CharField(required=False)
    criteria = forms.IntegerField(widget=forms.HiddenInput())
    value = forms.IntegerField(max_value=10, min_value=1)

ScoreFormSet = formset_factory(
    form = ReviewScoreForm,
    extra=0,
)