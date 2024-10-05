from django.urls import path
from .views import *

# Client user Working
urlpatterns=[
    path('home', home, name='home'),
    path('sending/file', upload_file, name='upload_file'),
    path('Sending/GenerateKey', keyview, name='keyview'),
    path('Receiver/Verifykey',keyaccess, name='keyaccess'),
    path('Receiver/Verified/<id>', download, name='download'),
]

# Giving path to our web pages to  perform task as they are builded...
urlpatterns += [
    path('login', loginuser, name='login'),
    path('create_user', create_user, name='CreateUser'),
    path('loggedIn/profile', update_user, name='UpdateUser'),
    path('logout', logoutuser, name='logout'),
]

urlpatterns+=[
    path('about', about, name='about'),
    path('about/developer', aboutdev, name='developer'),
]

