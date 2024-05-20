import os
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def slider_image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(
        "slider",
        str(instance.id),
        "%s%s" % (slugify(filename), extension)

    )


class HomePageSlider(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)
    slider_content = models.TextField(_("slider content"), blank=True)
    image = models.ImageField(_("image"), blank=True, null=True, upload_to=slider_image_upload_to)
    is_active = models.BooleanField(_("active"), default=True,
                                    help_text=_("Designates whether this slide is active."))
    homepageorder = models.PositiveSmallIntegerField(_("homepageorder"), null=True, blank=True, unique=True,
                                                     help_text=_("Order on homepage"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("homepageorder",)



