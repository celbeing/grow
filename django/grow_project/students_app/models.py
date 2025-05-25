from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.IntegerField()
    avatar_url = models.URLField(blank=True, null=True)  # 이후 아바타 페이지용

    def __str__(self):
        return f"{self.grade}학년 - {self.name}"
