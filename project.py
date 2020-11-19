import http.client

conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
    'x-rapidapi-key': "03e7e0d99cmshf91be55a6500328p140583jsn8da2cf74d30b"
    }

conn.request("GET", "/search?q=chicken", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))