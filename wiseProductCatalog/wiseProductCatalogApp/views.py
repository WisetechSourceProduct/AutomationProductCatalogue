from django.shortcuts import render
import requests
import pandas as pd
import re
import os
from datetime import datetime
import linecache
import logging
from django.conf import settings
import smtplib
from django.http import HttpResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)
#excel_file_path = "https://github.com/WisetechSourceProduct/AutomationProductCatalogue/raw/main/wiseProductCatalog/static/required_documents/wiseProductCatalogContentSheet.xlsx"
excel_file_path = "E:\Testsheet2.xlsx"



def create_folder(folder_name,static_dir):
    folder_path = os.path.join(static_dir, folder_name)
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created successfully at '{folder_path}'.")
        except OSError as error:
            logger.error("Exception occurred", exc_info=True)
            print(f"Failed to create folder '{folder_name}': {error}")


def download_file(file_link,key):

    if '/d/' not in file_link:
        return HttpResponse("Invalid file link format", status=400)
    
    # Extract the file ID from the link
    file_id = file_link.split('/d/')[1].split('/')[0]
    
    # Construct the direct download URL
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    # Fetch the file content
    response = requests.get(download_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[-1].strip('"')
        
        # Create an HTTP response with the file content
        file_response = HttpResponse(response.content, content_type=response.headers['Content-Type'])
        file_response['Content-Disposition'] = f'attachment; filename="{filename}"'
        static_file_path = os.path.join(settings.BASE_DIR, 'static', 'images',key,filename)
        if not os.path.exists(static_file_path):
            with open(static_file_path, 'wb') as static_file:
                static_file.write(response.content)
                print(static_file_path)
                print("created Successfully")
        return file_response
    else:
        return HttpResponse("Failed to download the file", status=500)


def download_vid_file(file_link,key):

    if '/d/' not in file_link:
        return HttpResponse("Invalid file link format", status=400)
    
    # Extract the file ID from the link
    file_id = file_link.split('/d/')[1].split('/')[0]
    
    # Construct the direct download URL
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    # Fetch the file content
    response = requests.get(download_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[-1].strip('"')
        
        # Create an HTTP response with the file content
        file_response = HttpResponse(response.content, content_type=response.headers['Content-Type'])
        file_response['Content-Disposition'] = f'attachment; filename="{filename}"'
        static_file_path = os.path.join(settings.BASE_DIR, 'static', 'videos',key,filename)
        if not os.path.exists(static_file_path):
            with open(static_file_path, 'wb') as static_file:
                static_file.write(response.content)
                print(static_file_path)
                print("created Successfully")
        return file_response
    else:
        return HttpResponse("Failed to download the file", status=500)


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
            print(products_dict[i][k][7])
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
        

def download_file_link(product):
    products_dict,products_logo_dict= products_dict_maker()
    for i,j in products_dict.items():
         for k in products_dict[i]:
            if k == product:

                product_slide_image = products_dict[i][k][6]
                product_slide_video = products_dict[i][k][7]
                return product_slide_image,product_slide_video
    return None  # Return None if the product is not found
   

    
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
        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
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
    subproducts_name = products_dictionary[0].get(product_name)
    return render(request,"wiseProductCatalogApp/subproducts.html", {"excel_data":content, "subproducts":subproducts_name,"productname":product_name})


def productdetails(request, product_name, product_details):
    try:
        key = product_details
        static_image_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        create_folder(key,static_image_dir)
        static_video_dir = os.path.join(settings.BASE_DIR, 'static', 'videos')
        create_folder(key,static_video_dir)
        img,vid = download_file_link(key)
        
        if vid != 'None':
            download_vid_file(vid,key)
        if img != 'None':
             file_link = img
             download_file(file_link,key)

        content = dict_maker(excel_file_path)
        products_dictionary = products_dict_maker()
        features_dictionary = features_dict_maker()[product_name][product_details]

        # Initialize image_urls
        image_urls = []

        # Image Directory of Carousel
        image_dir = os.path.join(settings.BASE_DIR, 'static', 'images', key)
        if os.path.exists(image_dir) and os.path.isdir(image_dir):
            image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
            if image_files:
                image_urls = ['images/' + key + '/' + image.replace('\\', '/') for image in image_files]

        # Fallback to default images if no specific images found
        if not image_urls:
            default_image_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'Default')
            if os.path.exists(default_image_dir) and os.path.isdir(default_image_dir):
                default_image_files = [f for f in os.listdir(default_image_dir) if os.path.isfile(os.path.join(default_image_dir, f))]
                if default_image_files:
                    image_urls = ['images/Default/' + image.replace('\\', '/') for image in default_image_files]

        # Video Directory of Carousel
        video_urls = []
        video_dir = os.path.join(settings.BASE_DIR, 'static', 'videos', key)
        if os.path.exists(video_dir) and os.path.isdir(video_dir):
            video_files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
            if video_files:
                video_urls = ['videos/' + key + '/' + video.replace('\\', '/') for video in video_files]

        if not video_urls:
            default_video_dir = os.path.join(settings.BASE_DIR, 'static', 'videos', 'Default')
            if os.path.exists(default_video_dir) and os.path.isdir(default_video_dir):
                default_video_files = [f for f in os.listdir(default_video_dir) if os.path.isfile(os.path.join(default_video_dir, f))]
                if default_video_files:
                    video_urls = ['videos/Default/' + video.replace('\\', '/') for video in default_video_files]

        context = {
            "excel_data": content,
            "subproducts": products_dictionary[0][product_name][product_details],
            "subproduct_name": product_details,
            "features": features_dictionary,
            'image_urls': image_urls,
            'video_urls': video_urls
        }

        return render(request, "wiseProductCatalogApp/productsdetail.html", context)
    
    except KeyError as e:
        logger.error("Exception occurred", exc_info=True)
        return HttpResponse("Product details not found", status=404)
    
    except Exception as e:
        logger.exception("An unexpected error occurred: %s", exc_info=True)
        return HttpResponse("An error occurred", status=500)


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


