import http.client
import json
from dal import autocomplete
import unicodedata

#API information
conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
    'x-rapidapi-key': "03e7e0d99cmshf91be55a6500328p140583jsn8da2cf74d30b"
    }
    
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def sanitizeInput(input):
    input=input.replace(" ","")
    input=input.strip()
    input=remove_control_characters(input)
    return input


