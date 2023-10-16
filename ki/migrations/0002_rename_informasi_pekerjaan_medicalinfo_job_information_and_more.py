# Generated by Django 4.2.6 on 2023-10-16 14:41

from django.db import migrations, models
import ki.models


class Migration(migrations.Migration):

    dependencies = [
        ('ki', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalinfo',
            old_name='informasi_pekerjaan',
            new_name='Job_Information',
        ),
        migrations.RenameField(
            model_name='personalinfo',
            old_name='alamat',
            new_name='Address',
        ),
        migrations.RenameField(
            model_name='personalinfo',
            old_name='email',
            new_name='Email',
        ),
        migrations.RenameField(
            model_name='personalinfo',
            old_name='nama',
            new_name='Full_Name',
        ),
        migrations.RenameField(
            model_name='personalinfo',
            old_name='no_ktp_paspor',
            new_name='ID_Number',
        ),
        migrations.RenameField(
            model_name='personalinfo',
            old_name='no_telepon',
            new_name='Phone',
        ),
        migrations.AlterField(
            model_name='medicalinfo',
            name='informasi_medis_file',
            field=models.FileField(upload_to='medical_info/', validators=[ki.models.validate_file_extension]),
        ),
    ]
