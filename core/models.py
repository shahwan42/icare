from django.db import models
from django.utils.translation import gettext_lazy as _


class CEntity(models.Model):
    """ClickUp entity base model"""

    c_id = models.PositiveIntegerField(_("ClickUp ID"), unique=True)
    is_active = models.BooleanField(_("is active?"), null=True)
    name = models.TextField(_("name"), max_length=2048, null=True)
    description = models.TextField(_("description"), null=True)

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

    class Meta:
        verbose_name = "ClickUp Team"
        verbose_name_plural = "ClickUp Teams"


class CSpace(CEntity):
    """ClickUp Space representation"""

    c_team = models.ForeignKey(
        CTeam, on_delete=models.CASCADE, related_name="spaces", null=True, blank=True
    )

    class Meta:
        verbose_name = "ClickUp Space"
        verbose_name_plural = "ClickUp Spaces"


class CFolder(CEntity):
    """ClickUp Folder representation"""

    c_space = models.ForeignKey(
        CSpace, on_delete=models.CASCADE, related_name="folders", null=True, blank=True
    )

    class Meta:
        verbose_name = "ClickUp Folder"
        verbose_name_plural = "ClickUp Folders"


class CList(CEntity):
    """ClickUp List representation"""

    c_folder = models.ForeignKey(
        CFolder, on_delete=models.CASCADE, related_name="lists", null=True, blank=True
    )

    # TODO in case of folderless lists, don't do it until asked strongly
    # force current structure for lower cost
    # c_space = models.ForeignKey(
    #     CSpace, on_delete=models.CASCADE, related_name="lists", null=True, blank=True
    # )

    class Meta:
        verbose_name = "ClickUp List"
        verbose_name_plural = "ClickUp Lists"


class CTask(CEntity):
    """ClickUp Task representation"""

    c_id = models.CharField(_("ClickUp ID"), max_length=12, unique=True)
    c_list = models.ForeignKey(
        CList, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )
    status = models.CharField(_("status"), max_length=100, blank=True)

    class Meta:
        verbose_name = "ClickUp Task"
        verbose_name_plural = "ClickUp Tasks"
