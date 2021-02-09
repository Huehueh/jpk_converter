import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

def is_xml_correct(input_filename):
    print("Sprawdzam", input_filename)
    request_url = "https://e-mikrofirma.mf.gov.pl/jpk-client/api/Jpk/Upload"
    mp_encoder = MultipartEncoder(
        fields={
            'jpk': (os.path.basename(input_filename), open(input_filename, 'rb'), 'text/xml')
        }
    )
    r = requests.post(
        request_url,
        data=mp_encoder,
        headers={'Content-Type': mp_encoder.content_type}
    )
    if r.status_code != 200:
        return None

    errors_list = r.json()[0]['validationErrors']
    # print(errors_list)
    return (len(errors_list) == 0)
