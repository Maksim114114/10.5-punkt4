import datetime
from django.conf import settings
from django.utils import timezone
from news.models import Category, Post, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task


@shared_task
def weekly_send_email_task():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in_post__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            # 'link': settings.SITE_URL,
            'link': f'{settings.SITE_URL}/news/',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю(runapscheduler.py)',
        body='',
        from_email='smax85@yandex.ru',
        # settings.EMAIL_HOST_USER_FULL,
        to=['maksimus114114@gmail.com', 'sel-max@mail.ru'],
        # subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()




# функция отправки сообщения подписчикам
def send_notifications(preview, pk, title, subscribers):#  то что будет в выходить в сообщении превью id title  и подписчики .
    html_content = render_to_string(
        'post_created_email.html',
        {
            'Text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers#отправляем подписчикам
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def sendemail_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add': #action событие которое сейчас происходит # post_add -создание статьи
        in_category = instance.categories.all() #class PostCategory /in_category
        subscribers: list[str] = []#все подписчики

        for category in in_category:
            subscribers = category.subscribers.all()
            subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)






@shared_task
def send_email_task(pk,instance):
    post = Post.object.get(pk=pk)
    categories = post.categories.all()
    title = post.title
    subscribers = []
    in_category = instance.categories.all()
    for category in in_category:
        subscribers = category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        for sub_user in subscribers:
            subscribers.append(sub_user.email)
    html_content = render_to_string(
        'post_created_email.html',
        {
            'Text': f'{post.title}',
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
#
