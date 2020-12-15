import http.client
import json
class Searcher:
    def __init__(self, keyword):
        self.keyword = keyword

    conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")
    headers = {
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
        'x-rapidapi-key': "03e7e0d99cmshf91be55a6500328p140583jsn8da2cf74d30b"
        }
    conn.request("GET", "/search?q="+keyword, headers=headers)

    res = conn.getresponse()
    raw_data = res.read()
    encoding = res.info().get_content_charset('utf8')  # JSON default
    data = json.loads(raw_data.decode(encoding))

    def jprint(obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    jprint(data)
