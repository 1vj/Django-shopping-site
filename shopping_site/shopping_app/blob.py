from django.core.files.base import ContentFile
import requests
def blob_to_image(url):

    file_name = url.split('/')[-1]
    print(file_name)
    return ContentFile(file_name)
print("returned response",blob_to_image('blob:http://localhost:3000/679a49e5-347d-474c-ac70-4d399db19b5b'))
