"""
Definition of views.
"""

from datetime import datetime
from http.client import HTTPResponse
from pickle import NONE
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'БарселонаТревел',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Вы можете связаться с нами любим удобным способом',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Подобрать тур',
            'message':'Поиск тура:',
            'year':datetime.now().year,
        }
    )
def links (request):
    """Renders the about links."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Идеи для отдыха',
            'message':'Популярные направления',
            'year':datetime.now().year,
            }
    )
def feedback (request):
    """Renders the feedback page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1':'Мужской', '2':'Женский'}
    recommendation = {'1':'Точно буду рекомендовать','2':'Вероятно порекомендую','3':'Не буду рекомендовать','4':'Затрудняюсь ответить'}
    if request.method == 'POST':
       form = FeedbackForm(request.POST)
       if form.is_valid():
           data = dict()
           data['name']=form.cleaned_data['name']
           data['gender']=gender[form.cleaned_data['gender']]
           data['recommendation']=recommendation[form.cleaned_data['recommendation']]
           if(form.cleaned_data['notice'] == True):
               data['notice']='Да'
           else:
               data['notice']='Нет'
           data['message']=form.cleaned_data['message']
           data['email']=form.cleaned_data['email']
           form=None
    else:
        form = FeedbackForm()
    return render(
        request,
           'app/feedback.html',
           {
              'form':form,
              'data':data
           }
       )   
def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
      regform = UserCreationForm (request.POST)
      if regform.is_valid(): #валидация полей формы
        reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
        reg_f.is_staff = False # запрещен вход в административный раздел
        reg_f.is_active = True # активный пользователь
        reg_f.is_superuser = False # не является суперпользователем
        reg_f.date_joined = datetime.now() # дата регистрации
        reg_f.last_login = datetime.now() # дата последней авторизации
        reg_f.save() # сохраняем изменения после добавления данных
        return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
          'regform': regform, # передача формы в шаблон веб-страницы
          'year':datetime.now().year,
        }
    )
def blog(request):
    """Renders the blog page"""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
       request,
       'app/blog.html',
       {
        'title':'Блог',
        'posts': posts, # передача списка статей в шаблон веб-страницы
        'year':datetime.now().year,
       }
    )
def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr) #запрос на выбор всех её комментариев

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
             comment_f = form.save(commit=False)
             comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
             comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
             comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
             comment_f.save() # сохраняем изменения после добавления полей
             return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
         form = CommentForm() # создание формы для ввода комментария
    return render(
         request,
         'app/blogpost.html',
         {
           'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
           'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
           'form': form, # передача формы добавления комментария в шаблон веб-страницы
           'year':datetime.now().year,
         }
    )

def newpost(request):
    """Renders the newpost page"""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": #после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save() #сохраняем изменения после добавления полей

            return redirect('blog') #переадресация на страницу Блог после создания статьи Блога
    else: 
        blogform = BlogForm() #создание объекта формы для вввода данных

    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,#передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )
def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видеообзоры',
            'message':'Мы подготовили для вас интересные видеообзоры:',
            'year':datetime.now().year,
        }
    )


