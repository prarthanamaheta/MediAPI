from celery import shared_task
from django.conf import settings

from MediDonor.models import Post
from MediUser.models import MediUser
from django.core.mail import send_mail


@shared_task(bind=True)
def send_mail_post(self, post_id):
    print('enter in celery')

    users = MediUser.objects.all()
    print(users)
    posts = Post.objects.get(id=post_id)
    print(posts)
    for user in users:
        mail_subject = "NEW Post!!!!"
        message = posts.title
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
        )
    print('**********')
    return 'Done!'

# def send_mail_donation(self):
