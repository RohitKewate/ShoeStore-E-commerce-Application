from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
from base.email import send_account_activation_email
from .models import Profile


#signals
def createProfile(sender,instance,created, **kwargs):
    try:
       if created:
           user = instance
           email_token = uuid.uuid4()
           profile = Profile.objects.create(
               user=user,
               name=user.first_name,
               email=user.email,
               username=user.username,
               email_token=email_token
           )

           email = user.email
           send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)


post_save.connect(createProfile, sender=User)