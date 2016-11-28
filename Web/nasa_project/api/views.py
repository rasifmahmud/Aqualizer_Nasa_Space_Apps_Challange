from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from rest_framework.authentication import SessionAuthentication, BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Task,WaterParticle,UserDevice,Standard
from api.serializers import TaskSerializer,WaterParticleSerializer
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import datetime

class Dummy():
    geoLocation = 'dummyGeo'

def login(request):
    if request.user.is_authenticated():
        queryset = WaterParticle.objects.filter(user  = request.user).order_by('dateTime')
        queryset2=Standard.objects.get(user = request.user)
        args={}
        if len(queryset)==0:
            dummy = Dummy()
            
            args={'water_data':queryset,'current_user':request.user, 'standard_data':queryset2,'current_data':dummy}
        else:
            args={'water_data':queryset,'current_user':request.user, 'standard_data':queryset2,'current_data':queryset.reverse()[0]}
        return render_to_response('loggedin.html', args)    
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html',c)

def guest_page(request):
    water_data = WaterParticle.objects.values('geoLocation').filter(access='public').distinct()
    return render_to_response('GuestPage.html',{'water_data':water_data})

def geo_detail(request,geo):
    water_data = WaterParticle.objects.filter(geoLocation=geo, access = 'public').order_by('dateTime')

    return render_to_response('GuestLoggedin.html',{'water_data':water_data} )


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password=password)
    if user is not None: 
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loading_main_page/')
    else:
        return HttpResponseRedirect('/accounts/invalid/')


def loading_main_page(request):
    return render_to_response('loading_main_page.html')
def loading_login_page(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html',c)


@login_required(login_url='/accounts/login/')
def loggedin(request):
    if request.user.is_authenticated():
        queryset = WaterParticle.objects.filter(user  = request.user).order_by('dateTime')
        queryset2=Standard.objects.get(user = request.user)
        args={}
        if len(queryset)==0:
            dummy = Dummy()
            
            args={'water_data':queryset,'current_user':request.user, 'standard_data':queryset2,'current_data':dummy}
        else:
            args={'water_data':queryset,'current_user':request.user, 'standard_data':queryset2,'current_data':queryset.reverse()[0]}
        return render_to_response('loggedin.html', args)    
    else:
        return HttpResponseRedirect('/accounts/login/')


def invalid_login(request):
    return HttpResponseRedirect('/accounts/logout/')
def logout(request):
    auth.logout(request)
    return render_to_response('loading_login_page.html')
def register_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        deviceID = request.POST.get('device_id')
        mobileNo = request.POST.get('mobile_no')
        access_type = request.POST.get('access_type')
        user, created = User.objects.get_or_create(username=user_name,email=email)
        user.set_password(password)
        user.save() 
        user_device = UserDevice(user = user_name,deviceID = deviceID, mobileNo = mobileNo,access=str(access_type).lower())
        user_device.save()  
        standard = Standard(user=user_name)
        standard.save()
        user = auth.authenticate(username = user_name, password=password)
        if user is not None: 
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/loading_main_page/')
        else:
            return HttpResponseRedirect('/accounts/invalid/')

    
    queryset = UserDevice.objects.all()
    args = {'all_user':queryset}
    args.update(csrf(request))
    return render_to_response('register.html', args)



def edit(request):
    if request.user.is_authenticated():


        if request.method == 'POST' and 'temp_set' in request.POST:
            from_temp = request.POST.get('from_temp')
            to_temp = request.POST.get('to_temp')
            data = Standard.objects.get(user=request.user)
            if len(from_temp)!=0:
                data.from_temperature = from_temp
                data.save()

            if len(to_temp)!=0:
                data.to_temperature = to_temp
                data.save()
            return HttpResponseRedirect('/accounts/edit/')
        

        elif request.method == 'POST' and 'ph_set' in request.POST:
            from_ph = request.POST.get('from_ph')
            to_ph = request.POST.get('to_ph')
            data = Standard.objects.get(user=request.user)
            if len(from_ph)!=0:
                data.from_ph = from_ph
                data.save()

            if len(to_ph)!=0:
                data.to_ph = to_ph
                data.save()
            return HttpResponseRedirect('/accounts/edit/')

        elif request.method == 'POST' and 'orp_set' in request.POST:
            from_orp = request.POST.get('from_orp')
            to_orp = request.POST.get('to_orp')
            data = Standard.objects.get(user=request.user)
            if len(from_orp)!=0:
                data.from_orp = from_orp
                data.save()

            if len(to_orp)!=0:
                data.to_orp = to_orp
                data.save()
            return HttpResponseRedirect('/accounts/edit/')

        elif request.method == 'POST' and 'sal_set' in request.POST:
            from_sal = request.POST.get('from_salinity')
            to_sal = request.POST.get('to_salinity')
            data = Standard.objects.get(user=request.user)
            if len(from_sal)!=0:
                data.from_salinity = from_sal
                data.save()

            if len(to_sal)!=0:
                data.to_salinity = to_sal
                data.save()
            return HttpResponseRedirect('/accounts/edit/')

        elif request.method == 'POST':
            
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            deviceID = request.POST.get('deviceID')
            mobileNo = request.POST.get('mobileNo')
            access_type = request.POST.get('pubradio')
            user = User.objects.get(username=request.user)
            user_device = UserDevice.objects.get(user = request.user)
            if len(mobileNo)!=0:
                    user_device.mobileNo = mobileNo
                    user_device.save()    
            
            if access_type is not None:
                if str(access_type)=='1':
                    user_device.access='public'
                    user_device.save()
                else:
                    user_device.access='private'
                    user_device.save()


            if len(email)!=0:
                    user.email=email
                    user.save()
            if len(password)!=0:
                    user.set_password(password)
                    user.save()
                    auth.logout(request)
                    return HttpResponseRedirect('/accounts/login/')

            
            return HttpResponseRedirect('/accounts/edit/')

        queryset1 = UserDevice.objects.get(user=request.user)
        queryset2 = User.objects.get(username = request.user)
        queryset3 = Standard.objects.get(user = request.user)
        args={'user_device':queryset1,'user':queryset2, 'data':queryset3,'current_user':request.user}
        args.update(csrf(request))
        return render_to_response('edit.html',args)

def register_success(request):
    queryset = WaterParticle.objects.filter(user  = request.user).order_by('dateTime')
    return render_to_response('loggedin.html', {'water_data':queryset,'current_user':request.user})

def get_orp():
    queryset = WaterParticle.objects.values('orp').filter(user='opu')
    if len(queryset)!=0:
        temp = queryset[random.randint(0,len(queryset)-1)]['orp']
        tempo= random.randint(0,1)
        if tempo==0:
            return temp+random.uniform(0,10)
        else:
            a=temp-random.uniform(0,10)
            if a<0:
                a=a*(-1)
            
            return a 
    else:
        return random.uniform(0,10)






@api_view(['GET','POST'])
def water_list(request,data):
    """
    List all tasks, or create a new task.
    """
    # tempo=get_orp()
    now=datetime.datetime.now()
    water_data = WaterParticle(user = 'opu',deviceID='aqualizer',geoLocation='23.8103*90.4125',dateTime=now)
    water_data.save()
    if request.method == 'GET':

        a = str(data).split("&")
        for i in a:
            temp = str(i).split("=")
            if str(temp[0])=='temperature':
                water_data.temperature = temp[1]
                water_data.save()
            elif str(temp[0])=='ph':
                water_data.ph = temp[1]
                water_data.save()
            elif str(temp[0])=='orp':
                water_data.orp = temp[1]
                water_data.save()


    if request.method == 'POST':
        a = str(data).split("&")
        for i in a:
            temp = str(i).split("=")
            if str(temp[0])=='temperature':
                water_data.temperature = temp[1]
                water_data.save()
            elif str(temp[0])=='ph':
                water_data.ph = temp[1]
                water_data.save()
            elif str(temp[0])=='orp':
                water_data.orp = temp[1]
                water_data.save()

                
    return Response(status=status.HTTP_201_CREATED)







@api_view(['GET'])
def water_detail(request, token):
    user_name = User.objects.values('username').filter(auth_token=token)
    if len(user_name)==0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        water = WaterParticle.objects.filter(user=user_name[0]['username'])
        serializer = WaterParticleSerializer(water,many=True)
        return Response(serializer.data)







@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

for user in User.objects.all():
    Token.objects.get_or_create(user=user)



@api_view(['GET','POST'])
def get_water(request):
    """
    List all tasks, or create a new task.
    """
    if request.method == 'GET':
        water_data = WaterParticle.objects.filter(user = 'opu')
        serializer = WaterParticleSerializer(water_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)





