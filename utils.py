from xml.etree.ElementTree import QName, SubElement, Element,register_namespace
import re

tags = {'os_fiz': 'http://crd.gov.pl/wzor/2020/05/08/9394/',
        'os_niefiz': 'http://crd.gov.pl/wzor/2020/05/08/9393/',
        'etd': 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2020/03/11/eD/DefinicjeTypy/'}

reps = {tags['os_fiz']: tags['etd']}
find_replacement = lambda m: reps[m.group(1)]
regex = r'({})'.format(r'|'.join(re.escape(w) for w in reps))

def registerNamespaces():
    for key, value in tags.items():
        register_namespace(key, value)


def getTnsaTag(tag : str, os_fiz : bool):
    return str(QName(tags['os_fiz' if os_fiz else 'os_niefiz'], tag))

def findTnsaElementWithTag(tag : str, document : Element) -> Element:
    for option in [True, False]:
        tnsa_tag = getTnsaTag(tag, option)
        # print(f"findTnsaElementWithTag {tnsa_tag}")
        list = document.findall(f'.//{tnsa_tag}')
        if len(list) != 0:
            return list[0]
    return None

def createTnsaSubElement(tag : str, os_fiz : bool, parent : Element):
    tnsa_tag = getTnsaTag(tag, os_fiz)
    new_element = SubElement(parent, tnsa_tag)
    return new_element

def changeTagOsFizToEtd(tag : str):
    return re.sub(regex, find_replacement, tag)