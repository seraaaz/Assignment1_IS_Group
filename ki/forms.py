from django import forms
from .models import User, PersonalInfo, MedicalInfo, BiometricData

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "id_card_image"]
        widgets = {
            "password": forms.PasswordInput(),
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['user']

    # Additional fields for PersonalInfo
    umur = forms.IntegerField(label='Age')
    tanggal_lahir = forms.DateField(label='Birthdate')

class MedicalInfoForm(forms.ModelForm):
    class Meta:
        model = MedicalInfo
        exclude = ['user']

    # Additional fields for MedicalInfo
    informasi_medis_file = forms.FileField(label='Upload Medical Information', required=False, widget=forms.FileInput)

class BiometricDataForm(forms.ModelForm):
    class Meta:
        model = BiometricData
        exclude = ['user']

    # Additional fields for BiometricDatag
    sidik_jari_image = forms.ImageField(label='Upload Fingerprint', widget=forms.FileInput)
