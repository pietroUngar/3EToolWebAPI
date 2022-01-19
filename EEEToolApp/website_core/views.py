from EEETools.Tools.API.ExcelAPI.modules_importer import calculate_excel
from EEETools.Tools.API.Tools.file_handler import get_file_position
from EEEToolApp.settings import MEDIA_ROOT
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ExcelUploadForm
from .models import ExcelFile
import os


DEFAULT_CONSOLE_MESSAGE = "Upload the compiled excel file in order to start the calculations"


def home(request):

    return __render_home(request, DEFAULT_CONSOLE_MESSAGE)


def download(request, filename=""):

    file_position = get_file_position(filename)

    if file_position == "" or not os.path.exists(file_position):

        console_message = "Unable to download!\nfile name:\t{}\nfile position:\t{}".format(filename, file_position)
        return __render_home(request, console_message)

    with open(file_position, 'rb') as file:

        response = HttpResponse(file.read(), content_type='application/adminupload')
        response['Content-Disposition']='inline;filename=' + filename

    return response


def clear_files(request):

    print(clear_files)
    objects = ExcelFile.objects.all()
    n_object = len(objects)

    for object in objects:

        object.delete()

    console_message = "{} Excel Files Deleted".format(n_object)
    return __render_home(request, console_message)


def calculate_and_download(request):

    if request.method == 'POST':

        console_text = "no excel file selected!"

        if len(ExcelFile.objects.all()) > 0:

            excel_path = os.path.join(MEDIA_ROOT, request.POST["select"])

            try:

                calculate_excel(excel_path)

            except:

                console_text = "error in the calculations!"

            else:

                with open(excel_path, 'rb') as file:

                    response = HttpResponse(file.read(), content_type='application/adminupload')
                    response['Content-Disposition'] = 'inline;filename=' + excel_path

                return response

        object_list = list()
        for object in ExcelFile.objects.all():
            object_list.append(str(object))

        return render(request, 'index.html', {

            "console_text": console_text,
            "form": ExcelUploadForm,
            "object_list": object_list

        })

    return __render_home(request, DEFAULT_CONSOLE_MESSAGE)


def __render_home(request, console_text):

    if request.method == 'POST':

        return __upload_excel(request)

    else:

        object_list = list()
        for object in ExcelFile.objects.all():
            object_list.append(str(object))

        return render(request, 'index.html', {

            "console_text": console_text,
            "form": ExcelUploadForm,
            "object_list": object_list

        })


def __upload_excel(request):

    form = ExcelUploadForm(request.POST, request.FILES)

    if form.is_valid():

        form.save()

    object_list = list()
    for object in ExcelFile.objects.all():
        object_list.append(str(object))
    console_text = "file saved"
    return render(request, 'index.html', {

            "console_text": console_text,
            "form": ExcelUploadForm,
            "object_list": object_list

        })

