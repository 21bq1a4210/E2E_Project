from django import forms
from user_administration.models import Class, Branch


class studentRegistrationForm(forms.Form):
    branches = Branch.objects.all()
    class_rooms = Class.objects.none()
    username = forms.CharField(label='Username', min_length=5, max_length=100, required=True)
    year = forms.IntegerField(min_value=1, max_value=4)
    class_room = forms.ModelChoiceField(queryset=class_rooms, label='Class')
    image = forms.FileField(label='Profile Image', required=False)
    roll_no = forms.CharField(min_length=10, max_length=10, required=True)
    branch = forms.ModelChoiceField(queryset=branches, label='Branch')
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'branch' in self.data:
            branch = self.data.get('branch')
            try:
                self.fields['class_room'].queryset = Class.objects.filter(branch_id=branch).order_by('-branch_id')
            except (ValueError, TypeError):
                pass


class studentLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
