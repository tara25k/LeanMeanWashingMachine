from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from django.core.files.storage import FileSystemStorage
from data.models import Data
from skimage import color
from skimage import io





global urlName
global title
def upload(request):
    global urlName
    global title
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        title = request.POST['title']
        print(title)

        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        with Image(filename=file_url) as img:
            img.colorspace = 'gray'
            img.save(filename='logo_gray.jpg')
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
    return render(request, 'website/success.html', {'descriptionArray': descriptionArray})


def successPage(request):
    return HttpResponseRedirect('Success')