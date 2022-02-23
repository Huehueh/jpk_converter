

from xml.etree.ElementTree import Element

form_v1_dict_m = {
    "kodSystemowy": "JPK_V7M (1)",
    "wersjaSchemy":"1-2E",
    }
form_v2_dict_m = {
    "kodSystemowy": "JPK_V7M (2)",
    "wersjaSchemy":"1-0E",
    }
form_v1_dict_k = {
    "kodSystemowy": "JPK_V7K (1)",
    "wersjaSchemy":"1-2E",
    }
form_v2_dict_k = {
    "kodSystemowy": "JPK_V7K (2)",
    "wersjaSchemy":"1-0E",
    }


dekl_v1_dict = {
    "kodSystemowy": "VAT-7 (21)",
    "wersjaSchemy":"1-2E",
    }
dekl_v2_dict = {
    "kodSystemowy": "VAT-7 (22)",
    "wersjaSchemy":"1-0E",
    }

def upgradeElement(element: Element):
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAA', element.attrib)
    if element.attrib == form_v1_dict_m:
        element.attrib = form_v2_dict_m
    if element.attrib == form_v1_dict_k:
        element.attrib = form_v2_dict_k
    if dekl_v1_dict.items() <= element.attrib.items():
        for key in dekl_v1_dict.keys():
            if key in dekl_v2_dict.keys():
                element.attrib[key] = dekl_v2_dict[key]
    if element.text == '21':
        element.text = '22'
    if element.text == '1':
        element.text = '2'
    print('Upgraded to', element.tag, element.attrib, element.text)
    return element
    
