from django import template
import re

register = template.Library()

@register.filter(name="url_convertor")
def url_convertor(text):
    pattern = "/[\w\-]{15,}/"
    converted_url = re.findall(pattern,text)
    return f"https://drive.google.com/thumbnail?id={converted_url[0].strip('/')}"

