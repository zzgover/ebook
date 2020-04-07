from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    belong_to = models.OneToOneField(User, on_delete=models.CASCADE,
                                     related_name='profile')
    real_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, default='12345678910')
    address = models.CharField(max_length=512)

    def __str__(self):

        return self.real_name + self.address

    # class Meta:
    #     fields='__all__'
