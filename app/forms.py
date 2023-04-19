"""
Definition of forms.
"""
from django.db import models
from.models import Comment
from.models import Blog

from pickle import FALSE
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _



class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
class FeedbackForm(forms.Form):
    """Форма обратной свзязи на сайте"""
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    email = forms.EmailField(label='Ваш e-mail', min_length=7, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                               choices=[('1','Мужской'),('2','Женский')],
                               widget = forms.RadioSelect,initial=1)                              
    message = forms.CharField(label='Ваш отзыв о путешествии', 
                              widget=forms.Textarea(attrs={'rows':8, 'cols':50}))
    recommendation = forms.ChoiceField(label='Порекомендуете ли наш сайт?',
                                        choices=(('1','Точно буду рекомендовать'),
                                                 ('2','Вероятно порекомендую'),
                                                 ('3','Не буду рекомендовать'),
                                                 ('4','Затрудняюсь ответить')), initial=1)
    notice = forms.BooleanField(label='Получать новости о скидках и горящих предложениях ',
                                required=False)

class CommentForm (forms.ModelForm):
    class Meta:
      model = Comment # используемая модель
      fields = ('text',) # требуется заполнить только поле text
      labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content':"Полное содержание", 'image': "Картинка"}

