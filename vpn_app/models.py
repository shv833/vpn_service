from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User


class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    url = models.URLField()
    page_views = models.PositiveIntegerField()
    data_transferred = models.FloatField()

