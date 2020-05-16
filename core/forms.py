from django import forms


class NewTaskFormInSpaces(forms.Form):
    def __init__(self, list_choices, *args, **kwargs):
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields["c_list"].choices = list_choices

    name = forms.CharField(label="العنوان")
    description = forms.CharField(
        label="الوصف", widget=forms.Textarea(attrs={"rows": 10, "cols": 30})
    )
    c_list = forms.ChoiceField(label="الفئة")


class NewTaskForm(forms.Form):
    """New task form to work with folders"""

    name = forms.CharField(label="العنوان")
    description = forms.CharField(
        label="الوصف", widget=forms.Textarea(attrs={"rows": 10, "cols": 30})
    )
    c_list = None

    def __init__(self, *args, **kwargs):
        folder = kwargs.pop("folder")
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields["c_list"] = forms.ModelChoiceField(
            label="الفئة",
            queryset=folder.lists.filter(is_active=True),
            empty_label="(default)",
        )
