from django.shortcuts import render
# Create your views here.
def home(request):
    print("Change")
    print("Change2")
    return render(request, "testingapp/home.html")