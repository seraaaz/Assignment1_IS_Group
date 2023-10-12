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
    umur = forms.IntegerField(label='Umur')
    tanggal_lahir = forms.DateField(label='Tanggal Lahir')

class MedicalInfoForm(forms.ModelForm):
    class Meta:
        model = MedicalInfo
        exclude = ['user']

    # Additional fields for MedicalInfo
    informasi_pekerjaan = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    informasi_medis_file = forms.FileField(label='Upload Informasi Medis', required=False, widget=forms.FileInput)

class BiometricDataForm(forms.ModelForm):
    class Meta:
        model = BiometricData
        exclude = ['user']

    # Additional fields for BiometricData
    sidik_jari_image = forms.ImageField(label='Upload Gambar Sidik Jari', widget=forms.FileInput)
