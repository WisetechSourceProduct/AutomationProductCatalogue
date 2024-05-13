from django.shortcuts import render
import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#excel_file_path = "https://github.com/WisetechSourceProduct/AutomationProductCatalogue/raw/main/wiseProductCatalog/static/required_documents/wiseProductCatalogContentSheet.xlsx"
excel_file_path = "E:\Testsheet.xlsx"




def excel_sheet_finder(excel_file):

    df = pd.ExcelFile(excel_file_path)
    return df.sheet_names # Returns sheet names as list


def dict_maker(excel_file): # function for convert excel file to dictionary

    df = pd.read_excel(excel_file, header=None)
    content = dict(zip(df[0], df[1]))
    return content


def products_dict_maker():

    products_dict = {}
    products_logo_dict = {}
    excel_header = []
    
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
    return products_dict, products_logo_dict



def features_dict_maker(): # Function for listing features and its icons
    
    features_dict = {}
    excel_header = []

    products_dataframe = pd.read_excel(excel_file_path, sheet_name="Products")
    for i in products_dataframe:
        excel_header.append(i)

    columns_to_fill = [excel_header[1], excel_header[4]]  # Specify the columns to fill
    products_dataframe[columns_to_fill] = products_dataframe[columns_to_fill].ffill() # it fills NaN value with previous row data
    products_dataframe_fillna = products_dataframe.fillna("None")

    for index, row in products_dataframe_fillna.iterrows():
        if row[excel_header[1]].rstrip(" \n") not in features_dict:
            features_dict[row[excel_header[1]].rstrip(" \n")] = {}
            if row[excel_header[4]].rstrip(" \n") not in features_dict[row[excel_header[1]].rstrip(" \n")]:
                features_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]].rstrip(" \n")] = []
                features_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]].rstrip(" \n")].append([row[excel_header[8]], row[excel_header[9]]])
            else:
                features_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]].rstrip(" \n")].append([*row[8:10]])
        else:
            try:
                features_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]].rstrip(" \n")].append([row[excel_header[8]], row[excel_header[9]]])
            except KeyError:
                features_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]]] = []
                features_dict[row[excel_header[1]].rstrip(" \n")][row[excel_header[4]].rstrip(" \n")].append([row[excel_header[8]], row[excel_header[9]]])
    return features_dict

def about_dict_maker():
    about_dict={}
    excel_header=[]

    products_dataframe = pd.read_excel(excel_file_path, sheet_name="About")
    for i in products_dataframe:
        excel_header.append(i)


    products_dataframe_fillna = products_dataframe.fillna("None")
    products_dataframe_fillna[excel_header[0]] =  products_dataframe[excel_header[0]].ffill() # it fills NaN value with previous row data
    
    for index, row in products_dataframe_fillna.iterrows():
        if row[excel_header[0]].rstrip(" \n") not in about_dict:
            about_dict[row[excel_header[0]].rstrip(" \n")] = {}
            about_dict[row[excel_header[0]].rstrip(" \n")][row[excel_header[1]]] = [*row[2:]]
            
        else:
            about_dict[row[excel_header[0]].rstrip(" \n")][row[excel_header[1]]] = [*row[2:]]

    return about_dict
        
    
    
    
    
def navbar_list_maker(): # This function need to be deleted after the evaluation.
    
    # Code for Navbar listing and findings 
    wiseNavbar_list = []
    excelSheet_header= []

    wiseNavbar_dataframe = pd.read_excel(excel_file_path, sheet_name=excel_sheet_finder(excel_file_path)[0]).ffill() # it fills NaN value with previous row data
    for i in wiseNavbar_dataframe:
        excelSheet_header.append(i)
    for index, row in wiseNavbar_dataframe.iterrows():
        if row[excelSheet_header[0]] == "wiseNavbar":
            wiseNavbar_list.append(row[excelSheet_header[1]])

    return wiseNavbar_list

def name_validation(name):

    if name == " ":
        message= "Plese Enter Any Name"
        return message

    elif len(name) < 3:
        message= "Plese Provide Valid Name"
        return message

    elif re.match(r"[a-zA-Z]{3,25}",name):
        message = "valid"
        return message
    else:
        message= "Plese Provide Valid Name"
        return message
    
def phone_validation(phone):
    if phone == " ":
        message= "Plese Enter Phone Number"
        return message
    
    elif re.match(r"[6-9]{1}[0-9]{2}[0-9]{3}[0-9]{4}",phone):
        message = "valid"
        return message
    
    else:
        message = "Plese Provide valid Phone Number"
        return message
    

def email_validation(email):
    if email == " ":
        message= "Plese Enter Any Email Address"
        return message
    
    if re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$",email):
        message = "valid"
        return message
    
    elif re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$",email):
        return message
    
    else:
        message = "Plese Provide valid Email Address"
        return message


def messsages_validation(messages):
    if messages == " ":
        message = "Plese Enter Any Messages"
        return message
    
    elif re.match(r"^[A-Za-z0-9.,\s]{10,}$",messages):
        message = "valid"
        return message

    else:
        message = "Plese Provide valid Message"
        return message

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Format the message
    message_text = message

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the MIME message
    msg.attach(MIMEText(message_text, 'plain'))

    # Create SMTP session for sending the mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Update with your SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return "Unable to send email"




# Create your views here.
def home(request):

    content = dict_maker(excel_file_path)
    return render(request, "wiseProductCatalogApp/home.html", {"excel_data":content, "excel_navbar":navbar_list_maker()}) # `excel_navbar` need to be removed after removing `navbar_list_maker` function


def products(request):

    products_dictionary = products_dict_maker()
    content = dict_maker(excel_file_path) 
    return render(request,"wiseProductCatalogApp/products.html",{"excel_data":content, "main_sector":products_dictionary[0].keys(), "main_sector_logo":products_dictionary[1]})


def subproducts(request, product_name):

    content = dict_maker(excel_file_path)
    products_dictionary = products_dict_maker()
    subproducts_name = products_dictionary[0].get(product_name) # Have to handle error on this area. If the key not found what will be the web page design
    return render(request,"wiseProductCatalogApp/subproducts.html", {"excel_data":content, "subproducts":subproducts_name,"productname":product_name})


def productdetails(request,product_name,product_details):
    
    
    content = dict_maker(excel_file_path) 
    products_dictionary = products_dict_maker()
    features_dictionary = features_dict_maker()[product_name][product_details]
    return render (request,"wiseProductCatalogApp/productsdetail.html",{"excel_data":content, "subproducts":products_dictionary[0][product_name][product_details], "subproduct_name":product_details, "features":features_dictionary})


def about(request):
    content = dict_maker(excel_file_path)
    about_dictionary = about_dict_maker()
    return render(request,"wiseProductCatalogApp/about.html",{"excel_data":content,"about_dictionary":about_dictionary})


def contact(request):
    content = dict_maker(excel_file_path)
    main_sector_data = products_dict_maker()
    error_list = []

    if request.method == "POST":
        product = request.POST.get('service')
        sub_product = request.POST.get('type-product')
        name = request.POST.get('fullname')
        fullname = name_validation(name)
        if fullname != "valid":
            error_list.append(fullname)

        email = request.POST.get('email')
        mail = email_validation(email)
        if mail != "valid":
            error_list.append(mail)

        phone = request.POST.get('phone')
        phone_num = phone_validation(phone)
        if phone_num != "valid":
            error_list.append(phone_num)

        message = request.POST.get('message')
        cus_message = messsages_validation(message)
        if cus_message != "valid":
            error_list.append(cus_message)

        if error_list:
            return render(request, "wiseProductCatalogApp/contact.html", {"excel_data": content, "main_sector_data": main_sector_data, "errors": error_list})
        
        # Extract sender email, password, and subject from content dictionary
        sender_email = content.get("sender_mail_id", "")
        sender_password = content.get("sender_password", "")
        subject = content.get("mail_subject", "")

        recipient_email = email
        mail_sent = send_email(sender_email, sender_password, recipient_email, subject, f"Name: {name}\nEmail: {email}\nPhone: {phone}\nProduct: {product}\nSub-product: {sub_product}\nMessage: {message}")

        if mail_sent == "Email sent successfully!":
            success_message = "Your message has been sent successfully!"
        else:
            success_message = "Failed to send the email. Please try again later."

        return render(request, "wiseProductCatalogApp/contact.html", {"excel_data": content, "main_sector_data": main_sector_data, "mail": mail_sent, "success_message": success_message})

    else:
        print("No Content is Coming")

    return render(request, "wiseProductCatalogApp/contact.html", {"excel_data": content, "main_sector_data": main_sector_data})


