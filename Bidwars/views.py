# total_item stands for search item or item that are inserted by user
# from email import message
# from django.conf import settings
# from django.http import response,HttpResponse
# from django.http.request import validate_host
from concurrent.futures import process
from click import command
from Bidwars.models import Register,Profile
from django.shortcuts import redirect, render
from django.contrib import messages
# from django.contrib.auth import authenticate, login
from datetime import datetime, time, timedelta, date
from .models import Register,Profile,Item,Store,Index
# from django.core.mail import BadHeaderError, send_mail
# from django.http import HttpResponse, HttpResponseRedirect
import smtplib
from email.message import EmailMessage
import re
import subprocess
import os
# import tempp as tp
# import time
# import fullimg_preprocess as fp

# Create your views here.

import cv2
import argparse
import subprocess
import os
import re
import numpy as np
#import image

#cv2.imshow('orig',image)
#cv2.waitKey(0)

# parser = argparse.ArgumentParser(description='Provide image path')
# parser.add_argument('img')
# args = parser.parse_args()


def get_result(img):
    command = (f'python main.py --img_file {img}').split()
    process=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)

    process_out= process.communicate()[0]
    process_out=str(process_out)
    return process_out

def full_preprocessing(img_path):
    result = list()
    output = list()
    image = cv2.imread(img_path)
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray',gray)
    # cv2.waitKey(0)

    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow('second',thresh)
    # cv2.waitKey(0)

    #dilation
    kernel = np.ones((5,100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    # cv2.imshow('dilated',img_dilation)
    # cv2.waitKey(0)

    #find contours
    ctrs,hier= cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        # show ROI
        # cv2.imshow('segment no:'+str(i),roi)
        name="segment_no_"+str(i)+".png"
        cv2.imwrite(name,roi)
        # os.path.join('/temp',name)
        # cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
        cv2.waitKey(0)
        result.append(get_result(name))

    for i in result:
        temp = re.findall("\".*\"",i)
        # print(temp)
        for j in temp:
            output.append(j)
    # print(result)
    # cv2.imwrite('final_bounded_box_image.png',image)
    # cv2.imshow('marked areas',image)
    # cv2.waitKey(0)
    return output
#if __name__ == '__main__':
# full_preprocessing(args.img)

def pricing(request):
   
    return render(request, 'pricing.html')
def error(request):
   
    return render(request, 'error.html')
# def get_result(img):
#     preprocess_file = str("D:\\Biddings-master\\Bidwars\\src\\fullimg_preprocess.py")
#     command = (f'python {preprocess_file} {img}').split()
#     process=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
#     output=process.communicate()[0]
#     output = str(output)
#     return output
    

def index(request):
    try:
        if request.method == "POST":
            # name = request.POST.get("image")
            image = request.FILES.get('image')
            adds = Index(image=image)
            print(image)
            adds.save()
            path = (f'D:/Biddings-master/media/media/{image}')
            # print(path)
            # print(get_result(path))
            output= full_preprocessing(path)
            ans = ''
            for i in range(len(output)-1, -1, -1):
                # ans += output[i] + ' '
                ans += output[i].replace('"', '') + '\n'
            # ans=ans[::-1]
            # print(ans)
            #code


            return render(request, 'show.html', {'image': image, 'ans' : ans})
    except Exception:
        return render(request, 'index.html')
    return render(request, 'index.html')

def search(request):
    try:
        if request.method == "GET":
            search = request.GET.get("search")
            search = search.lower()
            new_search = list(search.split(" "))
            search_file = open('search.txt','a')
            search_file.write("\n" + search)
            search_file.close()
            for i in new_search:
                #regex = r"^.*{}.*$".format(i)
                
                x = re.search("^.*["+i+"]*.*$",i).group()
                print(x,i)  
                reg = Item.objects.all().filter(total_item = x)
                print(reg)
            
            
            if not reg.exists():

                    
                    reg = Item.objects.all()
                    context = {
                        'res':'No result found. Showing results for..'
                        
                        
                    }
                    return render(request, 'search.html',{'reg':reg,'context':context})
    except Exception:
        return redirect('/error')           
                
        
      
        
    return render(request, 'search.html',{'reg':reg})

def about(request):
    return render(request, 'about.html')


def login(request):
    try:
        if request.method == "POST":
            
            
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #item = Item.objects.get(name=name,email=email)
           
            reg = Register.objects.get(name=name,email=email,password=password)
            
            return render(request, 'profile.html',{'reg':reg})
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Credentials!")
        
        return redirect('/login')

    return render(request, 'login.html')

def emails(request):
    reg = Register.objects.filter(email=request.session['email']).exists()
    if reg !=True:
        msg = EmailMessage()
        msg['Subject'] = 'Verification!!'
        msg['From'] = "atharvashirke77@gmail.com"
        msg['To'] = request.session['email']
        msg.set_content('''

<!DOCTYPE html>
<html>

<head>
    <title></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <style type="text/css">
        @media screen {
            @font-face {
                font-family: 'Lato';
                font-style: normal;
                font-weight: 400;
                src: local('Lato Regular'), local('Lato-Regular'), url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff) format('woff');
            }

            @font-face {
                font-family: 'Lato';
                font-style: normal;
                font-weight: 700;
                src: local('Lato Bold'), local('Lato-Bold'), url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff) format('woff');
            }

            @font-face {
                font-family: 'Lato';
                font-style: italic;
                font-weight: 400;
                src: local('Lato Italic'), local('Lato-Italic'), url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff) format('woff');
            }

            @font-face {
                font-family: 'Lato';
                font-style: italic;
                font-weight: 700;
                src: local('Lato Bold Italic'), local('Lato-BoldItalic'), url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff) format('woff');
            }
        }

        /* CLIENT-SPECIFIC STYLES */
        body,
        table,
        td,
        a {
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }

        table,
        td {
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }

        img {
            -ms-interpolation-mode: bicubic;
        }

        /* RESET STYLES */
        img {
            border: 0;
            height: auto;
            line-height: 100%;
            outline: none;
            text-decoration: none;
        }

        table {
            border-collapse: collapse !important;
        }

        body {
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }

        /* iOS BLUE LINKS */
        a[x-apple-data-detectors] {
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* MOBILE STYLES */
        @media screen and (max-width:600px) {
            h1 {
                font-size: 32px !important;
                line-height: 32px !important;
            }
        }

        /* ANDROID CENTER FIX */
        div[style*="margin: 16px 0;"] {
            margin: 0 !important;
        }
    </style>
</head>

<body style="background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;">
    <!-- HIDDEN PREHEADER TEXT -->
    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;"> We're thrilled to have you here! Get ready to dive into your new account. </div>
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <!-- LOGO -->
        <tr>
            <td bgcolor="#FFA73B" align="center">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td align="center" valign="top" style="padding: 40px 10px 40px 10px;"> </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#FFA73B" align="center" style="padding: 0px 10px 0px 10px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;">
                            <h1 style="font-size: 48px; font-weight: 400; margin: 2;">Welcome!</h1> <img src=" https://img.icons8.com/clouds/100/000000/handshake.png" width="125" height="120" style="display: block; border: 0px;" />
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0;">We're excited to have you get started. First, you need to confirm your account. Just press the button below.</p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" align="left">
                            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td bgcolor="#ffffff" align="center" style="padding: 20px 30px 60px 30px;">
                                        <table border="0" cellspacing="0" cellpadding="0">
                                            <tr>
                                            
                                                <td align="center" style="border-radius: 3px;" bgcolor="#FFA73B"><a href="http://biddings1.herokuapp.com/confirm" style="font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #FFA73B; display: inline-block;">Confirm Email</a></td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr> <!-- COPY -->
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 0px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0;">If that doesn't work, copy and paste the following link in your browser:</p>
                        </td>
                    </tr> <!-- COPY -->
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0;"><a href="#" target="_blank" style="color: #FFA73B;">https://bit.li.utlddssdstueincx</a></p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0;">If you have any questions, just reply to this email—we're always happy to help out.</p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0;">Cheers,<br>BBB Team</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#f4f4f4" align="center" style="padding: 30px 10px 0px 10px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td bgcolor="#FFECD1" align="center" style="padding: 30px 30px 30px 30px; border-radius: 4px 4px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <h2 style="font-size: 20px; font-weight: 400; color: #111111; margin: 0;">Need more help?</h2>
                            <p style="margin: 0;"><a href="#" target="_blank" style="color: #FFA73B;">We&rsquo;re here to help you out</a></p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td bgcolor="#f4f4f4" align="left" style="padding: 0px 30px 30px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;"> <br>
                            <p style="margin: 0;">If these emails get annoying, please feel free to <a href="#" target="_blank" style="color: #111111; font-weight: 700;">unsubscribe</a>.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>

    ''', subtype='html')


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("atharvashirke77@gmail.com", "@Atharvashirke.23")
            smtp.send_message(msg)
    else:
        
        messages.success(request, "Email Exists!")
        return render(request, 'register.html')

    return render(request, 'emails.html')
def confirm(request):   
    reg = Register.objects.filter(email=request.session['email']).exists()
    if reg != True:
        if request.session['plan'] == "Basic":
            date = datetime.today() + timedelta(days=25)
        elif request.session['plan'] == "Pro":
            date = datetime.today() + timedelta(days=45)
        else:
            date = datetime.today() + timedelta(days=365)

        registers = Register(name=request.session['name'], email=request.session['email'],
                                        password=request.session['password'],plan=request.session['plan'], date=date)

        registers.save()
        
        messages.success(request, "Registered Successfully!")
    else:
        messages.success(request, "Email exists!")
    return render(request, 'login.html')
def register(request):
    try:
        if request.method == "POST":
 
            request.session['name'] = request.POST.get('name')
            request.session['email'] = request.POST.get('email')
            request.session['password'] = request.POST.get('password')
            request.session['plan'] = request.GET.get('plan')

            reg = Register.objects.filter(email=request.session['email']).exists()
            
            
            
            
            if reg != True:
                return redirect('/emails')
            else:

                messages.error(request, "Email already exists!")
                return redirect('/register')
    except Exception as e:
        print(e)
        return redirect('/error')

    return render(request, 'register.html')

def profile(request):
    try:
       
        if request.method == "POST":
           
            name = request.POST.get("name")
            
            email = request.POST.get("email")
            password = request.POST.get("password")
            item = Item.objects.filter(name=name,email=email)
            pro = Profile.objects.filter(name=name, email=email).exists()
            
            if pro == True:
                pro = Profile.objects.get(name=name, email=email)
                reg = Register.objects.get(name=name,email=email,password=password)
                if reg.date >= date.today():
                    return render(request, 'profile.html',{'reg':reg, 'item':item, 'pro':pro})
                else:
                    messages.error(request, "Your free trial expired!")
                    return redirect('/register')
            else:
                pro = {
                    'address' : 'NA',
                    'phone' : 'NA',
                    'country' : 'NA'
                }
                reg = Register.objects.get(name=name,email=email,password=password)
                if reg.date >= date.today():
                    return render(request, 'profile.html',{'reg':reg, 'item':item, 'pro':pro})
                else:
                    messages.error(request, "Your free trial expired!")
                    return redirect('/register')
                
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Credentials")
        return redirect('/login')
        
    return render(request, 'profile.html')

def editpro(request):
    try:
        name = request.GET.get("name")
        email = request.GET.get("email")
        
        data = {'name':name,'email':email,}
        #email = request.POST.get("email")
        #password = request.POST.get("password")


        reg = Profile.objects.filter(email=email).exists()

        if reg != True:
            if request.method == "POST":
                #reg = Register.objects.filter(email=email).exists()
                
                address = request.POST.get('address')
                country = request.POST.get('country')
                phone = request.POST.get('phone')
                edit = Profile(name=name, email=email, phone = phone, 
                                        address=address, country=country)

                edit.save()
                
                messages.success(request, "Successfully edited your profile ")
                item = Item.objects.filter(name=name,email=email)
                reg = Register.objects.get(name=name,email=email)
                pro = Profile.objects.get(name = name, email = email)
                return render(request, 'profile.html',{'reg':reg,'item':item, 'pro':pro})
        else:

                messages.error(request, "Cant edit!")
                item = Item.objects.filter(name=name,email=email)
                reg = Register.objects.get(name=name,email=email)
                pro = Profile.objects.get(name = name, email = email)
                return render(request, 'profile.html',{'reg':reg,'item':item, 'pro':pro})
                
    except Exception:
       return redirect('/error')
        
    return render(request, 'editpro.pug',data) 

def add(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
   
    reg = Register.objects.get(name=name,email=email)
    try:
        if request.method == "POST":
            
            total_item = request.POST.get('total_item')
            gender = request.POST.get('gender')
            hobby = request.POST.get('hobby')
            income = request.POST.get('income')
            except_amount = request.POST.get('amount')
            age = request.POST.get('age')
            bio = request.POST.get('bio')
            image = request.FILES.get('image')
            item = Item.objects.filter(name=name,email=email)
            adds = Item(name=name, email=email,total_item=total_item,gender=gender,hobby=hobby,
                          income=income,except_amount=except_amount,age=age,bio=bio,image=image)
            adds.save()  
            pro = None    
            pro = Profile.objects.all().get(name = name, email = email)         
            print(name,total_item,email,gender,hobby,income,except_amount,age,bio,image)
            return render(request, 'profile.html',{'reg':reg,'item':item, 'pro':pro})
    except Exception as ee:
        print(ee)
        messages.error(request,'Urghh!')

        return render(request, 'profile.html',{'reg':reg,'item':item, 'pro':pro})
    return render(request, 'add.html',{'reg':reg})

def preview(request):
    product = Store.objects.all()
    return render(request, 'ECommerce-Website-design-master/index.html',{'product':product}) 

def product(request):
    if request.method == 'GET':
        product_name = request.GET.get('name')
        product = Store.objects.get(product_name = product_name)
        similar = Store.objects.all()
        
        
    return render(request, 'ECommerce-Website-design-master/product.html',{'product':product, 'similar':similar}) 


    #import subprocess
    #command = (f'python fullimg_preprocess.py {img}').split()
    #processs=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    #output=str(process.communicate())
    #python .\fullimg_preprocess.py "D:\Biddings-master\media\media\{image}"