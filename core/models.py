from django.db import models
from django.utils.translation import gettext_lazy as _


class CEntity(models.Model):
    """ClickUp entity base model"""

    c_id = models.PositiveIntegerField(_("ClickUp ID"), unique=True)
    is_active = models.BooleanField(_("is active?"))
    name = models.TextField(_("name"), max_length=2048)
    description = models.TextField(_("description"))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{__class__.__name__}, id: {self.c_id}>"


class CTeam(models.Model):
    """Starting point
    ClickUp Team representation"""

    c_id = models.PositiveIntegerField(_("ClickUp ID"), unique=True)
    name = models.CharField(_("name"), max_length=255)
    is_active = models.BooleanField(_("is active?"), default=True)


class CSpace(CEntity):
    """ClickUp Space representation"""

    c_team = models.ForeignKey(
        CTeam, on_delete=models.CASCADE, related_name="spaces", null=True, blank=True
    )


class CFolder(CEntity):
    """ClickUp Folder representation"""

    c_space = models.ForeignKey(
        CSpace, on_delete=models.CASCADE, related_name="folders", null=True, blank=True
    )


class CList(CEntity):
    """ClickUp List representation"""

    c_folder = models.ForeignKey(
        CFolder, on_delete=models.CASCADE, related_name="lists", null=True, blank=True
    )


class CTask(CEntity):
    """ClickUp Task representation"""

    c_id = models.CharField(_("ClickUp ID"), max_length=12, unique=True)
    c_list = models.ForeignKey(
        CList, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )
