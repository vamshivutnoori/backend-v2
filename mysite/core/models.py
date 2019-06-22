from django.db import models
from django.contrib.auth.models import User

class Products(models.Model):
	name=models.CharField(max_length=50)
	#last_name = models.Charfield(max_length=50)
	#email = models.EmailField()

	def __str__(self):
		return f'{self.name}'

class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriptions = models.CharField(max_length=1500, blank=True)
	
    def get_absolute_url(self):
        return reverse('mysite.core:user', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username
		
#class Contact(models.Model):
#	first_name=models.CharField(max_length=50)
#	last_name = models.Charfield(max_length=50)
#	email = models.EmailField()

#	def __str__(self):
#		return f'{self.first_name} {self.last_name}'