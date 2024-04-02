from django.shortcuts import render
import pandas as pd

excel_file_path = "https://github.com/WisetechSourceProduct/AutomationProductCatalogue/raw/main/wiseProductCatalog/static/required_documents/wiseProductCatalogContentSheet.xlsx"
# excel_file_path = "C:/Users/harih/Desktop/testSheet.xlsx"


def excel_sheet_finder(excel_file):
    df = pd.ExcelFile(excel_file_path)
    return df.sheet_names # Returns sheet names as list


def dict_maker(excel_file): # function for convert excel file to dictionary
    df = pd.read_excel(excel_file, header=None)
    content = dict(zip(df[0], df[1]))
    return content


# Create your views here.
def home(request):

    content = dict_maker(excel_file_path)

    # Code for Navbar listing and findings
    wiseNavbar_list = []
    excelSheet_header= []

    wiseNavbar_dataframe = pd.read_excel(excel_file_path, sheet_name=excel_sheet_finder(excel_file_path)[0]).ffill() # it fills NaN value with previous row data
    for i in wiseNavbar_dataframe:
        excelSheet_header.append(i)
    for index, row in wiseNavbar_dataframe.iterrows():
        if row[excelSheet_header[0]] == "wiseNavbar":
            wiseNavbar_list.append(row[excelSheet_header[1]])

    return render(request, "wiseProductCatalogApp/home.html", {"excel_data":content, "excel_navbar":wiseNavbar_list})


def products(request):

    products_dict = {}
    products_logo_dict = {}
    excel_header = []
    
    content = dict_maker(excel_file_path) # Convert excel file into dict format

    products_dataframe = pd.read_excel(excel_file_path, sheet_name="Products")
    for i in products_dataframe:
        excel_header.append(i)

    products_dataframe_fillna = products_dataframe.fillna("None")
    products_dataframe_fillna[excel_header[1]] =  products_dataframe[excel_header[1]].ffill() # it fills NaN value with previous row data

    for index, row in products_dataframe_fillna.iterrows():
        if row[excel_header[1]].rstrip(" \n") not in products_dict:
            if row[excel_header[2]] != "None":
                products_logo_dict[row[excel_header[1]].rstrip(" \n")] = row[excel_header[2]] # Coding for logo dictionary
            products_dict[row[excel_header[1]].rstrip(" \n")] = {}
            products_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]]] = [*row[5:]]
        else:
            products_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]]] = [*row[5:]]
    #print(products_dict)
    #print(products_logo_dict)

    """        
    for i in products_dict:
        for k in products_dict[i]:
            print(products_dict[i][k][1])
    """

    return render(request,"wiseProductCatalogApp/products.html",{"excel_data":content, "main_sector":products_dict.keys(), "main_sector_logo":products_logo_dict})


def subproducts(request):
    return render(request,"wiseProductCatalogApp/subproducts.html")