from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from django.core.files.storage import FileSystemStorage
from data.models import Data
from PIL import Image
import urllib.request
import os



global urlName
global title
global twillioURL
global mobileNumber
from django.views.decorators.csrf import ensure_csrf_cookie
from .tensorModel import tensorModel
import requests
@ensure_csrf_cookie
def getData(request):
    global mobileNumber
    if request.method == "POST":
        body = request.body
        imageUrl = request.POST.get('img_url')
        mobileNumber = request.POST.get('user_num')
        print(mobileNumber)
        print(imageUrl)
        r = requests.get(imageUrl)

        with open('sample.jpg', 'wb') as image:
            image.write(r.content)

        img = Image.open('sample.jpg').convert('L')
        img.save(os.path.abspath('grey')+'/'+'sample.jpg')
        return redirect('postData')
        return 200
    else:
        print(request.method)
        return 404




def upload(request):
    global urlName
    global title
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']



        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        img = Image.open(os.path.abspath('media')+'/'+os.path.basename((file_url))).convert('L')
        print(os.path.abspath('media')+'/'+os.path.basename((file_url)))
        title = tensorModel(os.path.abspath('media')+'/'+os.path.basename((file_url)))

        img.save(os.path.abspath('grey')+'/'+os.path.basename(file_url))
        urlName = str(file_url)
        return redirect('success')
    return render(request, 'website/uploadPage.html')

def success(request):
    global title
    titleArray = title.split(',')
    descriptionArray = []
    for title in titleArray:
        foundObject = Data.objects.filter(Name=title)
        descriptionArray.append(foundObject.first().Description)
    #if mobileNumber:
     #   return redirect('postData')
    #else:
    return render(request, 'website/uploadPage.html', {'descriptionArray': descriptionArray, 'successMessage':"Successfully Uploaded", 'link': 'http://127.0.0.1:8000'})

def postData(request):
    global mobileNumber
    global twillioURL
    twillioURL = 'http://4834-129-234-0-163.ngrok.io'
    r = requests.post(twillioURL + '/results', data={'content':'This is content', 'mobileNumber':mobileNumber})
    return render(request, 'website/uploadPage.html')