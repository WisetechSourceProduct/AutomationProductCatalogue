from django import template
import re

register = template.Library()

@register.filter(name="url_convertor")
def url_convertor(text):

    text = str(text)
    pattern = "/[A-Za-z0-9_-]{15,}/"
    if re.search("^https://drive.google.com/file/d/", text):        
        converted_url = re.findall(pattern,text)
        return f"https://drive.google.com/thumbnail?id={converted_url[0].strip('/')}"
    else:
        return text
    
@register.filter(name='split')
def split(value, key):
    points = []
    point = value.split(key)
    for i in point:
        points.append(i + "\n")
    return points
    