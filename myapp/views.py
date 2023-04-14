from django.http import HttpResponse
from django.shortcuts import render

from myapp.forms import SendOtpForm
from .models import *
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from twilio.rest import Client
from urllib.parse import unquote
from django.contrib.auth import authenticate, login
from twilio.rest import Client
from .models import User
from twilio.base.exceptions import TwilioRestException
from django.db.models import Q
from django.contrib import messages

# def send_otp(request):
#     if request.method == 'POST':
#         form = SendOtpForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data.get('name')
#             email = form.cleaned_data.get('email')
#             mobile_number = form.cleaned_data.get('mobile_number')

#             # Check if user with email or mobile number already exists
#             user = User.objects.filter(Q(email=email) | Q(mobile_number=mobile_number)).first()
#             if user is not None:
#                 error_message = 'A user with that email or mobile number already exists.'
#                 context = {'form': form, 'error_message': error_message}
#                 return render(request, 'send_otp.html', context=context)
#             else:

#                 # return redirect('send_otp')
            
#                 # Generate an OTP using the Twilio Verify API
#                 account_sid = "AC1114c2b6981bb296484425b66235f1ae"
#                 auth_token = "a967a5e590ce4139086af0a178f6e824"
#                 verification_sid = "VA71aecf834b5caf4696289d5167f48381"
#                 client = Client(account_sid, auth_token)
#                 verification = client.verify.services(verification_sid).verifications.create(to='+91' + mobile_number, channel='sms')

#                 # Store the user's details and verification_sid in the session
#                 request.session['name'] = name
#                 request.session['email'] = email
#                 request.session['mobile_number'] = mobile_number
#                 request.session['verification_sid'] = verification.sid

#                 print(name)
#                 print(email)
#                 print(mobile_number)
#                 print(verification.sid)
            
#                 # Redirect to the verify OTP view
#                 return redirect('verify_otp')
#         else:
#             form = SendOtpForm()

#             context = {'form': form}
#             return render(request, 'send_otp.html', context=context)

#     elif request.method == 'GET':
#         return render(request, 'send_otp.html')

def send_otp(request):
    error_message = None  # Define error_message outside of if blocks

    if request.method == 'POST':
        form = SendOtpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            mobile_number = form.cleaned_data.get('mobile_number')

            # Check if user with email or mobile number already exists
            user = User.objects.filter(Q(email=email) | Q(mobile_number=mobile_number)).first()
            if user is not None:
                error_message = 'A user with that email or mobile number already exists.'
                context = {'form': form, 'error_message': error_message}
                return render(request, 'send_otp.html', context=context)
            else:

                # Generate an OTP using the Twilio Verify API
                account_sid = "AC1114c2b6981bb296484425b66235f1ae"
                auth_token = "a967a5e590ce4139086af0a178f6e824"
                verification_sid = "VA71aecf834b5caf4696289d5167f48381"
                client = Client(account_sid, auth_token)
                verification = client.verify.services(verification_sid).verifications.create(to='+91' + mobile_number, channel='sms')

                # Store the user's details and verification_sid in the session
                request.session['name'] = name
                request.session['email'] = email
                request.session['mobile_number'] = mobile_number
                request.session['verification_sid'] = verification.sid

                print(name)
                print(email)
                print(mobile_number)
                print(verification.sid)
            
                # Redirect to the verify OTP view
                return redirect('verify_otp')
        else:
            # Add error message to context
            error_message = 'A user with that email or mobile number already exists.'
            context = {'form': form, 'error_message': error_message}
            return render(request, 'send_otp.html', context=context)

    elif request.method == 'GET':
        form = SendOtpForm()
        context = {'form': form}
        return render(request, 'send_otp.html', context=context)


def verify_otp(request):
    if request.method == 'POST':
        # Get user input from the form
        otp = request.POST.get('otp')
       # Retrieve the user's details and verification_sid from the session
       
        mobile_number = request.session.get('mobile_number')
        name = request.session.get('name')
        email = request.session.get('email')
        verification_sid = "VA71aecf834b5caf4696289d5167f48381"
        print(verification_sid)

        # Validate the OTP using the Twilio Verify API
        account_sid = "AC1114c2b6981bb296484425b66235f1ae"
        auth_token = "a967a5e590ce4139086af0a178f6e824"
        client = Client(account_sid, auth_token)
        try:
            verification_check = client.verify.v2.services(verification_sid) \
                .verification_checks \
                .create(to='+91'+mobile_number, code=otp)
            print(verification_check.status)


            if verification_check.status == 'approved':
                # If the OTP is valid, create a user object in the database
                user = User(name=name, email=email, mobile_number=mobile_number, otp_validated=True)
                user.save()

                return HttpResponse("registered")
            else:
                # If the OTP is invalid, show an error message to the user
                context = {'name': name, 'email': email, 'mobile_number': mobile_number}
                return render(request, 'verifyotp.html', {'error': 'Wrong OTP!'})
        except TwilioRestException as e:
            # Handle Twilio API errors and return an appropriate response
            return render(request, 'verify_otp.html', {'error': 'Wrong OTP!'})
        
    elif request.method == 'GET':
        # Retrieve the user's details and verification_sid from the session
        mobile_number = request.session.get('mobile_number')
        name = request.session.get('name')
        email = request.session.get('email')
        verification_sid = request.session.get('verification_sid')
        print(verification_sid)
        context = {'name': name, 'email': email, 'mobile_number': mobile_number}
        return render(request, 'verify_otp.html', context=context)

