from EEETools.Tools.API.ExcelAPI.modules_importer import calculate_excel
from EEETools.Tools.API.Tools.file_handler import get_file_position
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import EEEToolApp.settings as settings
from django.http import HttpResponse
import os


fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "excel_files"))
DEFAULT_CONSOLE_MESSAGE = "Upload the compiled excel file in order to start the calculations"


def home(request):

    console_text = DEFAULT_CONSOLE_MESSAGE

    if request.method == 'POST':

        try:

            return __upload_excel(request)

        except:

            console_text = "Error in file upload!"

    return __render_home(request, console_text)


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

    file_list = __get_file_list()
    n_object = len(file_list)

    if n_object == 1:

        pm = ""

    else:

        pm = "S"

    console_message = "{} EXCEL FILE{} DELETED".format(n_object, pm)

    file_name = ""

    try:

        for file_name in file_list:

            fs.delete(file_name)

    except Exception as e:

        console_message = "ERROR IN DELETING A FILE:\nEXCEL NAME:\n{}\n\nERROR:\n{}".format(file_name, e)

    return __render_home(request, console_message)


def calculate_and_download(request):

    console_text = DEFAULT_CONSOLE_MESSAGE

    if request.method == 'POST':

        console_text = "NO EXCEL FILE SELECTED!"

        if len(__get_file_list()) > 0:

            select_result = request.POST["select"]
            excel_path = ""

            for file_name in __get_file_list():

                if str(file_name) == select_result:
                    excel_path = file_name

            try:

                calculate_excel(fs.path(excel_path))

            except Exception as e:

                import platform
                console_text = "ERROR:\n{}\n\nEXCEL PATH:\n{}\n\nIS PATH:\n{}\n\nCURRENT OS:\n{}".format(e, excel_path, os.path.exists(excel_path), platform.system())

            else:

                with open(fs.path(excel_path), 'rb') as file:

                    response = HttpResponse(file.read(), content_type='application/adminupload')
                    response['Content-Disposition'] = 'inline;filename=' + excel_path

                return response

    return __render_home(request, console_text)


def __render_home(request, console_text):

    return render(request, 'index.html', {

        "console_text": console_text,
        "object_list": __get_file_list()

    })


def __upload_excel(request):

    uploaded_file = request.FILES["excel_file"]
    fs.save(uploaded_file.name, uploaded_file)

    console_text = "file saved"
    return __render_home(request, console_text)


def __get_file_list():

    return fs.listdir(fs.base_location)[1]


