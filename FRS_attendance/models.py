from django.db import models
from user_administration.models import CustomUser
from django.utils import timezone

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"

    class Meta:
        unique_together = ('user', 'date')  # Ensure attendance is marked only once per day for a user


class FaceRegistration(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    face_features = models.BinaryField(null=True, blank=True)  # Store the face features in binary format
    face_image = models.ImageField(upload_to='face_images/', null=True, blank=True)  # Store the face image

    def __str__(self):
        return f"{self.user.username}'s Face Registration"
