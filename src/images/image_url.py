from image_search import search

class Images:
    def search_museum(self, name: str, num_results = 5) -> dict:
        
        results = search(name)
        result = results["results"]

        data: dict = {}
        for i in range(num_results):
            key_image = "image_" + str(i)
            data[key_image] = result[i]["image"]
            key_thumb = "thumbnail_" + str(i)
            data[key_thumb] = result[i]["thumbnail"]
        return data

img = Images()
test = img.search_museum("1000 islands museum")