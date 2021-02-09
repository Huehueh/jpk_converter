from xml.etree import ElementTree
from xml.etree.ElementTree import QName, Element, SubElement, register_namespace
import re
from test import is_xml_correct

tags = {'tnsa': 'http://crd.gov.pl/wzor/2020/05/08/9394/',
        'etd': 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2020/03/11/eD/DefinicjeTypy/'}

for key, value in tags.items():
    register_namespace(key, value)

def getTnsaElementWithTag(tag : str, document : Element):
    tnsa_tag = str(QName(tags['tnsa'], tag))
    list = document.findall(f'.//{tnsa_tag}')
    if len(list) == 0:
        return None
    return list[0]

def getTnsaTag(text : str):
    return str(QName(tags['tnsa'], text))

def updateOsobaFizyczna(document : Element):
    reps = {tags['tnsa']: tags['etd']}
    names_to_change = ['NIP', 'ImiePierwsze', 'Nazwisko', 'DataUrodzenia']
    tags_to_change = [f"{{{tags['tnsa']}}}{name}" for name in names_to_change]
    find_replacement = lambda m : reps[m.group(1)]
    regex = r'({})'.format(r'|'.join(re.escape(w) for w in reps))

    os_fiz = getTnsaElementWithTag('OsobaFizyczna', document)
    if os_fiz is None:
        print("W dokumencie nie ma pola 'Osoba fizyczna'")

    for element in os_fiz:
        if element.tag in tags_to_change:
            print(f"Zmieniam {element.tag}")
            element.tag = re.sub(regex, find_replacement, element.tag)

def createTnsaSubElement(text : str, parent : Element):
    tag = str(QName(tags['tnsa'], text))
    new_element = SubElement(parent, tag)
    new_element.text = "0"

def updateZakupySprzedaze(document : Element):
    options = {'SprzedazCtrl' : ['LiczbaWierszySprzedazy', 'PodatekNalezny'],
               'ZakupCtrl' : ['LiczbaWierszyZakupow', 'PodatekNaliczony']}

    section = 'Ewidencja'
    pole_ewidencja = getTnsaElementWithTag(section, document)
    for option in options.keys():
        element = getTnsaElementWithTag(option, document)
        if element == None:
            tag = getTnsaTag(option)
            print(f"Dodaję pole {tag} w polu Ewidencja")
            new_element = SubElement(pole_ewidencja, tag)
            for subelem_title in options[option]:
                createTnsaSubElement(subelem_title, new_element)


document = ElementTree.parse('test.XML')
root = document.getroot()
updateOsobaFizyczna(root)
updateZakupySprzedaze(root)

output_filename = 'output.xml'
with open(output_filename, 'w') as output_file:
    output_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    output_file.write(ElementTree.tostring(root, encoding='utf-8').decode())

good = is_xml_correct(output_filename)
if good == None:
    print("Nie można sprawdzić poprawności pliku!")
else:
    print("XML poprawny!" if good else "XML niepoprawny:(")


