from django.db import models
from django.contrib.auth.models import User

class BackupRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    backup_time = models.DateTimeField(auto_now_add=True)
    backup_type = models.CharField(max_length=50, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')])

    class Meta:
        ordering = ['-backup_time']

        def __str__(self):
            return f"{self.user.username} - {self.backup_time} ({self.backup_type})"
