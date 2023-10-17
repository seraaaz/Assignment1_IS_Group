from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, PersonalInfoForm, MedicalInfoForm, BiometricDataForm
from hashfunctions import cryptoHasher
from .models import User
from django.core.files.storage import default_storage
import os
from django.http import HttpResponse
import datetime

EncryptionAlgo = "ARC4"

hasher = cryptoHasher.Hasher()


# Your view remains the same
def upload_success(request):
    return render(request, "ki/upload_success.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "ki/login.html")


def download_data(request, file_type):
    if request.user.is_authenticated:
        current_user = request.user
        file = None
        content_type = None

        if file_type == 'id_card_image':
            # Download ID Card Image
            file = current_user.id_card_image
            content_type = "image/jpeg"  # Adjust the content type accordingly

        elif file_type == 'informasi_medis_file':
            # Download Medical Info File
            file = current_user.medicalinfo.informasi_medis_file
            content_type = "application/pdf"  # Adjust the content type accordingly

        elif file_type == 'sidik_jari_image':
            # Download Fingerprint Image
            file = current_user.biometricdata.sidik_jari_image
            content_type = "image/jpeg"  # Adjust the content type accordingly

        if file:
            response = HttpResponse(file, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename={file.name}'
            return response

    return redirect("login")

# def download_data(request, file_type):
#     if request.user.is_authenticated:
#         current_user = request.user
#         file = None
#         content_type = None

#         if file_type == 'id_card_image':
#             # Download ID Card Image
#             file = current_user.id_card_image
#             content_type = "image/jpeg"  # Adjust the content type accordingly

#         elif file_type == 'informasi_medis_file':
#             # Download Medical Info File
#             file = current_user.medicalinfo.informasi_medis_file
#             content_type = "application/pdf"  # Adjust the content type accordingly

#         elif file_type == 'sidik_jari_image':
#             # Download Fingerprint Image
#             file = current_user.biometricdata.sidik_jari_image
#             content_type = "image/jpeg"  # Adjust the content type accordingly

#         if file:
#             response = HttpResponse(file, content_type=content_type)
#             response['Content-Disposition'] = f'attachment; filename={file.name}'
#             return response

#     return redirect("login")


# def download_data(request, file_name):
#     if request.user.is_authenticated:
#         current_user = request.user

#         # get the user's data
#         personal_info = User.objects.get(username=current_user.username).personalinfo
#         medical_info = User.objects.get(username=current_user.username).medicalinfo
#         biometric_data = User.objects.get(username=current_user.username).biometricdata

#         # decrypt the files
#         id_card_image, id_card_image_path = hasher.decryptFile(
#             current_user.id_card_image.path, EncryptionAlgo, key=current_user.password
#         )
#         informasi_medis_file, informasi_medis_file_path = hasher.decryptFile(
#             medical_info.informasi_medis_file.path,
#             EncryptionAlgo,
#             key=current_user.password,
#         )
#         sidik_jari_image, sidik_jari_image_path = hasher.decryptFile(
#             biometric_data.sidik_jari_image.path,
#             EncryptionAlgo,
#             key=current_user.password,
#         )

#         # return view with the data

#         # DOWNLOAD THE FILES
#         response = HttpResponse(id_card_image, content_type="application/vnd.ms-excel")
#         response["Content-Disposition"] = "inline; filename=" + os.path.basename(
#             id_card_image_path
#         )
#         return response

#         return render(
#             request,
#             "ki/download_data.html",
#             {
#                 "personal_info": personal_info,
#                 "medical_info": medical_info,
#                 "biometric_data": biometric_data,
#             },
#         )
#     else:
#         return redirect("login")


def upload_data(request):
    if request.method == "POST":
        now = datetime.datetime.now()
        user_form = UserForm(request.POST, request.FILES)
        personal_info_form = PersonalInfoForm(request.POST)
        medical_info_form = MedicalInfoForm(request.POST, request.FILES)
        biometric_data_form = BiometricDataForm(request.POST, request.FILES)

        if (
            user_form.is_valid()
            and personal_info_form.is_valid()
            and medical_info_form.is_valid()
            and biometric_data_form.is_valid()
        ):
            # Save User data
            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password"]
            file = request.FILES["id_card_image"]

            file_name = default_storage.save("id_cards/" + file.name, file)
            print("File Name: ", file_name)

            path_to_file = os.path.abspath("media/" + file_name)
            print("Path to File: ", path_to_file)

            user = User.objects.create_user(
                username=username, password=password, id_card_image=path_to_file
            )

            # Save PersonalInfo data with the related User instance
            personal_info = personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.save()

            # Save MedicalInfo data with the related User instance
            medical_info = medical_info_form.save(commit=False)
            medical_info.user = user
            medical_info.save()

            medical_info.informasi_medis_file = hasher.encryptFile(
                medical_info.informasi_medis_file.path,
                EncryptionAlgo,
                key=user.password,
            )
            medical_info.save()

            # Save BiometricData data with the related User instance
            biometric_data = biometric_data_form.save(commit=False)
            biometric_data.user = user
            biometric_data.save()

            biometric_data.sidik_jari_image = hasher.encryptFile(
                biometric_data.sidik_jari_image.path, EncryptionAlgo, key=user.password
            )
            biometric_data.save()

            # delete old files
            hasher.deleteFile(user.id_card_image.path, ".jpg")
            hasher.deleteFile(medical_info.informasi_medis_file.path, ".pdf")
            hasher.deleteFile(biometric_data.sidik_jari_image.path, ".jpg")

            deltatime = datetime.datetime.now() - now
            print("Delta Time: ", deltatime.total_seconds())
            return redirect("upload_success")  # Replace with your success URL.

    else:
        user_form = UserForm()
        personal_info_form = PersonalInfoForm()
        medical_info_form = MedicalInfoForm()
        biometric_data_form = BiometricDataForm()

    return render(
        request,
        "ki/upload_data.html",
        {
            "user_form": user_form,
            "personal_info_form": personal_info_form,
            "medical_info_form": medical_info_form,
            "biometric_data_form": biometric_data_form,
        },
    )


@login_required
def profile(request):
    current_user = request.user

    # Get the user's data
    personal_info = User.objects.get(username=current_user.username).personalinfo
    medical_info = User.objects.get(username=current_user.username).medicalinfo
    biometric_data = User.objects.get(username=current_user.username).biometricdata

    return render(
        request,
        "ki/profile.html",
        {
            "personal_info": personal_info,
            "medical_info": medical_info,
            "biometric_data": biometric_data,
        },
    )
