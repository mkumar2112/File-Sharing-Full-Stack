from .models import User
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import random
import string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
import os


# SuperUser -> monu -> monu1234

def GenerateKey():
    characters =  string.digits +string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(16))


def sendEmail(senderemail=None, receiveremail=None, message=None):
    if not senderemail or not receiveremail or not message:
        # print("Sender email, receiver email, and message must be provided.")
        return

    try:
        sendername = User.objects.get(email=senderemail)
        sendername = f"{sendername.first_name} {sendername.last_name}".strip()
    except ObjectDoesNotExist:
        # print(f"Sender with email {senderemail} does not exist.")
        return

    try:
        receivername = User.objects.get(email=receiveremail)
        receivername = f"{receivername.first_name} {receivername.last_name}".strip()
    except ObjectDoesNotExist:
        # print(f"Receiver with email {receiveremail} does not exist.")
        return

    # print(f"Sending email from {sendername} to {receivername}.")

    # Sending the email
    try:
        if not message: 
            message = f"Hi {receivername or receiveremail}, \n\n Your friend has sended you some documents please visit our web site. \n\n http://127.0.0.1:8000/home "
        else:
            message = f"Hi {receivername or receiveremail}, \n\n Your friend has sended you some documents please visit our web site. \n\n You got some message from your {sendername }.\n {message}. \n\n Visit our website. http://127.0.0.1:8000/home "

        send_mail(
            subject='You have a new message',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiveremail],
            fail_silently=False,
        )
        # print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")



# sendEmail("abc@gmail.com", "monukumar20238@gmail.com", "Testing Message")




def home(request):
    return render(request, 'home.html')

# Request for login Page if user were enter correct password and user id than login other wise return to again login page
def loginuser(request):
    if request.method =='POST':
        user = request.POST.get('user_n') # Taking user-id from web page
        password = request.POST.get('pass') # Taking password from web page
        # Checking login Credintals
        user = authenticate(username=user, password=password) # if user is authenticated than user login else user = None
        # print(user, password)
        if user is not None: # Checking User is not None
             # A  backend authenticated the credentials
             login(request, user) # Login to application
             return redirect("/sending/file") # Goes to loged in web page
        else:
             # No backend authenticated the credentials
             return render(request, 'login.html') # Return to login
    return render(request, 'login.html')


# Request to create user

def create_user(request):
    if request.method == 'GET':
        form = RegisterForm() # A registration Form is creating.
        return render(request, 'create_user.html', { 'form': form}) 
    if request.method == 'POST':
        form = RegisterForm(request.POST) # A registration Form is creating.
        if form.is_valid(): # if form is valid.
            user = form.save(commit=True) 
            user.username = user.username.lower()
            user.save() # Form save
            login(request, user)
            return redirect('/login')  # Return to login
        else:
            return render(request, 'create_user.html', {'form': form})  # Return to User creation Form


@login_required(login_url='/home')
def update_user(request):
    user = request.user
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            # Save user details
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # Update password if provided and valid
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)  # Keep user logged in after password change
            user.save()
            return redirect('/loggedIn/profile')  # Redirect to a profile page or wherever you want

    return render(request, 'profile.html', {'form': form})

#Log-out User
@login_required(login_url='/home')
def logoutuser(request):
    logout(request) #pre-define Function
    return redirect('/home') # return to home page







@login_required(login_url='/home')
def upload_file(request):
    if request.method == 'POST':
        form = SendFile(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['File']
            notes = form.cleaned_data['Notes']
            email = form.cleaned_data['Email']

            if uploaded_file:  # Check if a file was uploaded
                # Create an instance of the Files model
                file_instance = Files(
                    File=uploaded_file,
                    Note=notes,
                    key=GenerateKey(), 
                    Email = email # Generate a new key
                    # sender=request.user,  # Set the sender to the logged-in user
                    # receiver=None  # Set receiver if applicable
                )
                # print(file_instance.key)
                # Save the instance to the database
                file_instance.save()
                user_email = request.user.email  # Get the logged-in user's email
                sendEmail(user_email, email, notes)

                # Redirect to a success page or a detail view of the uploaded file
                return redirect(f'/Sending/GenerateKey?key={file_instance.key}')  # Change '/success/' to your desired URL
    else:
        form = SendFile() 
    
    return render(request, 'SendingFile.html', {'form': form})

@login_required(login_url='/home')
def keyview(request):
    key = request.GET.get('key') 
    if key:
        return render(request, 'KeyThankNote.html', {'message':'Your File has sended.', 'key': key})
    else:
        return HttpResponse('No key')

@login_required(login_url='/home')
def keyaccess(request):
    key = request.POST.get('key')
    user_email = request.user.email
    if key:
        Fileinstance = Files.objects.get(key=key[:16])
        ReceiverEmail = Fileinstance.Email
        # print(ReceiverEmail , user_email)
        if user_email != ReceiverEmail:
            return render(request , 'Keyaccess.html', {"message": " You are not eligible for these documents."})
        
        return redirect(f'/Receiver/Verified/{Fileinstance.id}')
    
        
    return render(request , 'Keyaccess.html')



@login_required(login_url='/home')
def download(request, id=None):
    if id is not None:
        document = get_object_or_404(Files, id=id)

        # Prepare the response for the file download
        response = HttpResponse(document.File, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={document.File.name}'  # Use .name to get the file name

        # Get the file path from the File instance
        file_path = document.File.path  # Use .path to get the full file system path

        # Remove the file from the server after the download
        if os.path.exists(file_path):
            os.remove(file_path)  # Correctly remove the file from the file system
            # Optionally delete the database entry
            document.delete()  # Delete the database record

        return response
    
    return redirect('/Receiver/Verifykey')

def about(request):
    return render(request, 'about.html')

def aboutdev(request):
    return render(request, 'aboutdev.html')

