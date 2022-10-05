from django.db import models


class SiteInfo(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='Logo')
    logo = models.ImageField(upload_to='Logo')

    def __str__(self):
        return self.name
