from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from .models import Profile 
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import PermissionDenied
from django.contrib.auth import  logout

# @receiver(user_logged_in)
# def deny_login(sender, request, user, **kwargs):
#     if not user.is_superuser and user.ldap_user is not None and ("Καθηγητής" not in user.ldap_user._user_attrs._data.get('title') or  "Ιδρυματικός Λογαριασμός" not in user.ldap_user._user_attrs._data.get('title')):
#         logout(request)
#         raise PermissionDenied('You do not have permission to access this resource.')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, department=instance.department, title=instance.title)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()
    #check if it is a postgrad student
    if "Καθηγητής" in instance.profile.title:
        #if its the first time to login, create a student profile and alert office.
        my_group = Group.objects.get(name='professors') 
        my_group.user_set.add(instance)
    elif "Ιδρυματικός Λογαριασμός" in instance.profile.title :
        instance.is_staff=True
        if "Πληροφορικής και Τηλεματικής" in instance.profile.department :
            my_group = Group.objects.get(name='secretary_dit') 
            my_group.user_set.add(instance)
        elif "Γεωγραφίας" in instance.profile.department :
            my_group = Group.objects.get(name='secretary_geo') 
            my_group.user_set.add(instance)
        elif "Διατροφολογίας" in instance.profile.department :
            my_group = Group.objects.get(name='secretary_geo') #TODO change this when I add this group
            my_group.user_set.add(instance)
        elif "Οικιακής" in instance.profile.department :
            my_group = Group.objects.get(name='secretary_geo') #TODO change this when I add this group
            my_group.user_set.add(instance)
    else :
        my_group = Group.objects.get(name='students') 
        my_group.user_set.add(instance)
