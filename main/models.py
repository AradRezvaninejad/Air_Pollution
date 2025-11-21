from django.db import models


# Create your models here.
class EducationCard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="info")  # Feather icon name
    color_from = models.CharField(max_length=20, default="blue-400")  # gradient start
    color_to = models.CharField(max_length=20, default="blue-600")  # gradient end
    order = models.PositiveIntegerField(default=0)  # برای ترتیب نمایش

    def __str__(self):
        return self.title


class Article(models.Model):

    title = models.CharField(max_length=200)
    summary = models.TextField()
    image_url = models.ImageField(
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    published_date = models.DateField()
    read_time = models.PositiveIntegerField(help_text="Time to read in minutes")
    link = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
