from django.shortcuts import render
import pandas as pd

# Create your views here.
def home(request):

    df = pd.read_excel("https://github.com/WisetechSourceProduct/AutomationProductCatalogue/raw/main/wiseProductCatalog/static/required_documents/testSheet.xlsx", header=None)
    
    content = dict(zip(df[0], df[1])) # Convert excel file into dict format
    
    return render(request, "wiseProductCatalogApp/home.html",{"excel_data":content} )

def products(request):
    return render(request,"wiseProductCatalogApp/products.html")