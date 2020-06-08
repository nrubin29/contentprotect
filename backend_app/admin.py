from django.contrib import admin

from backend_app.models import HashedImage, ImageMatch

admin.site.register(HashedImage)
admin.site.register(ImageMatch)
