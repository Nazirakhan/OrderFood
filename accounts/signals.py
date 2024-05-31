from django.db.models.signals import post_save, pre_save
from .models import User, UserProfile
from django.dispatch import receiver

@receiver(post_save, sender = User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        # print('create profile')
        UserProfile.objects.create(user=instance)
        # print('User Profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            # print('User is updated')
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
        #     print("User Profile not exist, but created one")
        # print('User is updated')

@receiver(pre_save, sender = User)
def pre_save_user_profile(sender, instance, **kwargs):
    # print(instance.username, 'This user is being saved')
    pass