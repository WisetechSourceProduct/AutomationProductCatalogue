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
    
@register.filter(name='splitter')
def splitter(value, key):
    point = value.split(key)
    return point
    
@register.filter(name='readmore')
def readmore(value,max_length):
    if len(value) > max_length:
        truncated_value = value[:max_length] + '...'
        return truncated_value
    else:
        return value
    
@register.filter(name='append_to_list')
def append_to_list(list, value):
    list.append(value)
    return list

@register.filter(name='init_list')
def init_list(value):
    return []