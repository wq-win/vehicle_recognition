from django.test import TestCase

# Create your tests here.
from User.models import User

print(User.objects.get(pk=10).u_icon.path)
print(User.objects.get(pk=10).u_icon.url)
print(User.objects.get(pk=10).u_icon.name)
