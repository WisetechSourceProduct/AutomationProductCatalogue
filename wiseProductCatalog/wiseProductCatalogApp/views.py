from django.shortcuts import render
import pandas as pd

excel_file_path = "https://github.com/WisetechSourceProduct/AutomationProductCatalogue/raw/main/wiseProductCatalog/static/required_documents/wiseProductCatalogContentSheet.xlsx"
# Create your views here.
def home(request):

    df = pd.read_excel(excel_file_path, header=None)
    content = dict(zip(df[0], df[1])) # Convert excel file into dict format
    return render(request, "wiseProductCatalogApp/home.html",{"excel_data":content} )


def products(request):

    df = pd.read_excel(excel_file_path, header=None)
    content = dict(zip(df[0], df[1])) # Convert excel file into dict format
    return render(request,"wiseProductCatalogApp/products.html",{"excel_data":content})