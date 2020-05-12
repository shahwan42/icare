from django.db import models
from django.utils.translation import gettext_lazy as _


class CEntity(models.Model):
    """ClickUp entity base model"""

    c_id = models.PositiveIntegerField(_("ClickUp ID"), unique=True)
    is_active = models.BooleanField(_("is active?"))
    name = models.TextField(_("name"))
    description = models.TextField(_("description"))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{__class__.__name__}, id: {self.c_id}>"


class CSpace(CEntity):
    """ClickUp Space representation"""


class CFolder(CEntity):
    """ClickUp Folder representation"""


class CList(CEntity):
    """ClickUp List representation"""


class CTask(CEntity):
    """ClickUp Task representation"""

    c_id = models.CharField(_("ClickUp ID"), max_length=12, unique=True)
