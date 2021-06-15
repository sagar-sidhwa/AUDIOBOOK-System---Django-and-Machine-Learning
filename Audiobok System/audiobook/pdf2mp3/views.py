from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import sys
import datetime
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth import authenticate, login, logout
from pdf2mp3.models import Audiobookuser,Pdf,Pdftemp

#For Pdf to Mp3 Converter
from gtts import gTTS
from pygame import mixer
from PIL import Image
import pytesseract
import os
import glob
import fitz
import PyPDF2
from fpdf import FPDF
# Create your views here.

# In this function we get first and last page, which we want the software to read

global e,first_page_number,last_page_number,gd,ffd

gd = os.getcwd()
mfdd = '\\pdf2mp3\\f'
ffd = gd+mfdd

print('Current Dir',gd)

def get_text(value):
    string = value
    string = string.strip()
    if "-" in string:
        first_page_number = int(string.split("-")[0])
        last_page_number = int(string.split("-")[1])
    else:
        first_page_number = int(string)
        last_page_number = 0
        
    return first_page_number,last_page_number

def pdf2mp3working(pdf_to_read,final_directory,first_page_number,last_page_number,mp3name):
    # In this bunch of code, we get permission to delete the folder if it already exists, where we intend to save our PDF images and audio
    image_directory = glob.glob(final_directory)
    for file in os.listdir(final_directory):
        filepath = os.path.join(final_directory,file)
        print(filepath)
        os.chmod(filepath, 0o777)
        os.remove(filepath)

    # Here we read desired PDF pages and store them as images in a folder
    doc = fitz.open(pdf_to_read)
    k=1
    # If user wants to read a single page
    if last_page_number == 0:
        page = doc.loadPage(first_page_number-1) #number of page
        zoom_x = 2.0
        zoom_y = 2.0
        mat = fitz.Matrix(zoom_x,zoom_y)
        pix = page.getPixmap(matrix=mat)
        output = os.path.join(final_directory, r"image_to_read.png")
        pix.writePNG(output)

    # If user wants to read range of pages
    else:
        for i in range(first_page_number-1,last_page_number):
            page = doc.loadPage(i) #number of page
            zoom_x = 2.0
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x,zoom_y)
            pix = page.getPixmap(matrix=mat)
            output = os.path.join(final_directory, r"image_"+str(k)+"_to_read.png")
            pix.writePNG(output)
            k+=1

    print("Done")

    # Initialize the Pytesseract OCR software
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe" 

    mytext = []

    # Here we load the image(s) created in Text_to_speech folder and read the text in image via pytesseract Optical Character Recognition (OCR) software
    # thus reading text in images and giving us a string
    for file in os.listdir(final_directory):
        data = pytesseract.image_to_string(Image.open(os.path.join(final_directory,file)),lang="eng")
        data = data.replace("|","I") # For some reason the image to text translation would put | instead of the letter I. So we replace | with I
        data = data.split('\n')
        mytext.append(data)

    # Language in which you want to convert 
    language = 'en'
    print(mytext)

    # Here we make sure that the text is read correctly and we read it line by line. Because sometimes, text would end abruptly
    newtext= ""
    for text in mytext:
        for line in text:
            line = line.strip()
            # If line is small, ignore it
            if len(line.split(" ")) < 10 and len(line.split(" "))>0:
                newtext= newtext + " " + str(line) + "\n"
            elif len(line.split(" "))<2:
                pass
            else:
                if line[-1]!=".":
                    newtext = newtext + " " + str(line)
                else:
                    newtext = newtext + " " + line + "\n"
                    
    print(newtext)

    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=newtext, lang=language, slow=False) 
            
    # Saving the converted audio in a mp3 file named pdf_audio.mp3
    myobj.save(os.path.join(ffd,mp3name))
    return myobj


#Views.py Functions

def home(request):
    if len(request.POST)==0:
        return render(request,'home.html')
    else:
        ud = request.POST['idetails']
        usid = Audiobookuser.objects.filter(id=ud)
        return render(request,'home.html',{'usid':usid})

def login(request):
    if len(request.POST)==0:
        return render(request,'login.html')
    else:
        mail = request.POST['email']
        password = request.POST['password']
        uid=Audiobookuser.objects.filter(email=mail,password=password)
        up=''
        for u in uid:
            up = u.password
            ud = u.id
            print('user id is',ud)
        if up == password:
            usid = Audiobookuser.objects.filter(id=ud)
            pdft = Pdftemp.objects.filter(uu=ud)
            return render(request,'details.html',{'pdft':pdft,'usid':usid})
        if up =='':
            emessage="Please Provide valid Details"
            return render(request,'login.html',{'emessage':emessage})
        

def register(request):
    if len(request.POST)==0:
        return render(request,'register.html')    
    else:
        name = request.POST['name']
        sname = request.POST['sname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        t=Audiobookuser(name=name,sname=sname,email=email,password=password,cpassword=cpassword)
        t.save()
        usid = Audiobookuser.objects.filter(name=name,sname=sname,email=email,password=password,cpassword=cpassword)
        for us in usid:
            us_id=us.id
        pdft = Pdftemp.objects.filter(uu=us_id)
        return render(request,'details.html',{'pdft':pdft,'usid':usid})


def upload(request):
    if len(request.POST)==0:
        return render(request,'upload.html')
    elif request.POST['idetails'] != 0:
        ud = request.POST['idetails']
        usid = Audiobookuser.objects.filter(id=ud)
        return render(request,'upload.html',{'usid':usid})
    
def uploadi(request):
    if len(request.POST)==0:
        return render(request,'upload.html')
    else:
        ud = request.POST['idetails']
        pdf = request.FILES['pdf']
        aname = request.POST['aname']
        arange = request.POST['arange']
        dt = datetime.datetime.now()

        first_page_number,last_page_number = get_text(arange)

        gf='\\pdf2mp3\\f\\Test\\Text_to_speech_software'
        gdr = '\\pdf2mp3\\f\\Test\\'
        mdr = '\\pdf2mp3\\f\\'
        final_directory = gd+gf
        #fd = 'E:/Tempt/HMI/audiobook/pdf2mp3/f/Test/Text_to_speech_software/'
        dr = gd+gdr

        fpdf=pdf
        
        fs = FileSystemStorage(location=dr) #defaults to   MEDIA_ROOT  
        filename = fs.save(fpdf.name, fpdf)
        pname = filename

        #file_url = fs.url(filename)
        pdf_to_read=dr+filename
        print('path',dr+filename)

        mp3name = aname+'.mp3'
        #Run Function
        mp3timepass = pdf2mp3working(pdf_to_read,final_directory,first_page_number,last_page_number,mp3name)

        #mp3dir = gd+mdr
        mp3 = mp3name #str(mp3dir+mp3name)
        #p = Pdf(dt=dt,u=ud,pname=pname,arange=arange,pdf=pdf,aname=aname,mp3=mp3)
        #p.save()

        print(mp3,type(mp3))
        uud=Audiobookuser(id=ud)
        tt = Pdftemp(ddt=dt,uu=uud,ppname=pname,aarange=arange,ppdf=pdf,aaname=aname,mmp3=mp3)
        print('Done')
        tt.save()

        '''print(pdf,type(pdf))
        print(aname,type(aname))
        print(arange,type(arange))
        print(dt,type(dt))
        '''
        #usid = Audiobookuser.objects.filter(id=1)
        #pdft = Pdftemp.objects.filter(uu=usid)
        ud = request.POST['idetails']
        usid = Audiobookuser.objects.filter(id=ud)
        pdft = Pdftemp.objects.filter(uu=ud)
        return render(request,'details.html',{'pdft':pdft,'usid':usid})

def details(request): 
    if len(request.POST)==0:
        return render(request,'details.html')
    else:
        ud = request.POST['idetails']
        usid = Audiobookuser.objects.filter(id=ud)
        #for us in usid:
        #us_id=us.id
        pdft = Pdftemp.objects.filter(uu=ud)
    #pdft = Pdftemp.objects.all()
        return render(request,'details.html',{'pdft':pdft,'usid':usid})


def detailsi(request):
    usid = Audiobookuser.objects.filter(id=1)
    pdft = Pdftemp.objects.all()
    return render(request,'details.html',{'pdft':pdft})

'''
,{'pdft':pdft,'usid':usid}
'''


gf='\\pdf2mp3\\f\\Test\\Text_to_speech_software'
gdr = '\\pdf2mp3\\f\\Test\\'
mfdd = '\\pdf2mp3\\f'
mdr = '\\pdf2mp3\\f\\'
finaldirectory = gd+gf #final_directory
#For Pdf 
directory = gd+gdr #dr
mp3save = gd+mfdd
mp3dir = gd+mdr #mp3 = str('E:/Tempt/HMI/audiobook/pdf2mp3/f/'+mp3name)

print('Added Final Dir',finaldirectory)
print('Added Pdf Dir',directory)
print('Mp3 Saving',mp3save)
print('Mp3 Directory',mp3dir)