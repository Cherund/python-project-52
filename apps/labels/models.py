from django.db import models
from django.utils.translation import gettext_lazy as _



# Create your models here.
class Label(models.Model):
    name = models.CharField(_('name'), max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
