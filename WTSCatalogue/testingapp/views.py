from django.shortcuts import render
# Create your views here.
def home(request):
    print("Change")
    return render(request, "testingapp/home.html")