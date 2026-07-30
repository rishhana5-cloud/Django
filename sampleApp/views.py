from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
     a=['apple','banana','orange','manago']
     return render(request,'app2/home.html',{'abc':a})
    # return HttpResponse('<h1>WELCOME TO HOME</h1>')
def about(request):
    # return HttpResponse('<h1>WELCOME TO ABOUT</h1>')
    return render(request,'app2/about.html')