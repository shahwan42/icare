from django import forms


class NewTaskForm(forms.Form):
    """New task form to work with folders"""

    name = forms.CharField(label="العنوان")
    description = forms.CharField(
        label="الوصف", widget=forms.Textarea(attrs={"rows": 10, "cols": 30})
    )
    due_date = forms.DateTimeField(
        # input_formats=["%d/%m/%Y"],
        label="موعد التسليم",
        required=False,
        widget=forms.DateTimeInput(
            format=("%d-%m-%Y"), attrs={"type": "date", "min": "2020-1-1"},
        ),
    )
    _list = None

    def __init__(self, *args, **kwargs):
        folder = kwargs.pop("folder")
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields["_list"] = forms.ModelChoiceField(
            label="الفئة",
            queryset=folder.lists.filter(is_active=True),
            empty_label="------",
        )
