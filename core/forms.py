from django import forms


class NewTaskForm(forms.Form):
    def __init__(self, list_choices, *args, **kwargs):
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields["c_list"].choices = list_choices

    name = forms.CharField(label="العنوان")
    description = forms.CharField(
        label="الوصف", widget=forms.Textarea(attrs={"rows": 10, "cols": 30})
    )
    c_list = forms.ChoiceField(label="الفئة")
