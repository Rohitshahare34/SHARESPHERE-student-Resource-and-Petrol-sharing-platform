from django.db import models

class Users(models.Model):
    usn = models.CharField(max_length=10, primary_key=True)
    dob = models.DateField()
    password = models.CharField(max_length=255)  # Store hashed passwords in production
    name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    contact_number = models.BigIntegerField()
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.name
