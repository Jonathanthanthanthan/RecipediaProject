from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio=models.TextField(max_length=256, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                   related_name='rel_from_set',
                                   on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                 related_name='rel_to_set',
                                 on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                               db_index=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# This code creates a new field called following that will be added to the User model 
following = models.ManyToManyField('self',
                                    through=Contact,
                                    related_name='followers',
                                    symmetrical=False)

# This code adds the 'following' field to the django user model without having to extend the user model. 
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                        through=Contact,
                        related_name='followers',
                        symmetrical=False))




