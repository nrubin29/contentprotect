from django.contrib.auth.models import User
from django.db import models


class HashedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    image_hash = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class ImageMatch(models.Model):
    hashed_image = models.ForeignKey(HashedImage, on_delete=models.CASCADE)
    permalink = models.CharField(max_length=500)

    @property
    def url(self):
        return 'https://reddit.com' + self.permalink

    def __str__(self):
        return self.permalink
