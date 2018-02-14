from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# https://github.com/wassgha/FaceRecognitionAPI/blob/master/api/views.py 에 있는 패키지
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import base64
#from PIL import Image
from io import StringIO
import urllib.request

from subprocess import Popen, PIPE

# Constants
bounding_region = 30 # Default: 30
thresh_val = 200 # Default: 230
lower_area_limit = 100 # Default: 100
upper_area_limit = 25000 # Default: 25000
circ_score_thresh = 1.55 # Default: 1.55
r_effective = 1.25 # Radius of pupil to center of eyeball


def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        process = Popen(['python', './scripts/eye_analysis.py', '.' + uploaded_file_url, '-jpg'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
   

        return render(request, 'core/home.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'core/home.html')
