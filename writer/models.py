from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, null=True, blank=True)
    # profile_picture = models.ImageField(
    #     upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_fields(self):
        return [(field.verbose_name, getattr(self, field.name)) for field in self._meta.fields]

    # def get_absolute_url(self):
    #     return reverse_lazy('author_list')

    # @classmethod
    # def get_model_label(cls):
    #     return cls._meta.verbose_name_plural

    # class Meta:
    #     verbose_name = _("Professor")
    #     verbose_name_plural = _("Professors")
