from xml.etree import ElementTree
from xml.etree.ElementTree import QName, Element, SubElement, register_namespace
import re
import xml.dom.minidom as minidom

tags = {'tnsa': 'http://crd.gov.pl/wzor/2020/05/08/9394/',
        'etd': 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2020/03/11/eD/DefinicjeTypy/'}

for key, value in tags.items():
    register_namespace(key, value)

def prettify(elem : Element):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def getTnsaElementWithTag(tag : str):
    tnsa_tag = str(QName(tags['tnsa'], tag))
    list = document.findall(f'.//{tnsa_tag}')
    if len(list) == 0:
        return None
    return list[0]

def updateOsobaFizyczna(document : Element):
    reps = {tags['tnsa']: tags['etd']}
    names_to_change = ['NIP', 'ImiePierwsze', 'Nazwisko', 'DataUrodzenia']
    tags_to_change = [f"{{{tags['tnsa']}}}{name}" for name in names_to_change]
    find_replacement = lambda m : reps[m.group(1)]
    regex = r'({})'.format(r'|'.join(re.escape(w) for w in reps))

    os_fiz = getTnsaElementWithTag('OsobaFizyczna')
    # os_fiz_tag = str(QName(tags['tnsa'], 'OsobaFizyczna'))
    # os_fiz = document.findall(f'.//{os_fiz_tag}')
    # if len(os_fiz) == 0:
    #     return

    if os_fiz is None:
        print("W dokumencie nie ma pola 'Osoba fizyczna'")

    for element in os_fiz:
        print (element.tag, element.text)
        if element.tag in tags_to_change:
            element.tag = re.sub(regex, find_replacement, element.tag)
        print(element.tag, element.text)


def updateZakupySprzedaze(document : Element):
    options = {'SprzedazCtrl' : ['LiczbaWierszySprzedazy', 'PodatekNalezny'],
               'ZakupCtrl' : ['LiczbaWierszyZakupow', 'PodatekNaliczony']}

    ew_tag = str(QName(tags['tnsa'], 'Ewidencja'))
    ewidencja = document.findall(f'.//{ew_tag}')
    if len(ewidencja) < 1:
        print("Brak elementu ewidencja")
        return 1
    print(ewidencja[0])

    for option in options.keys():
        tag = str(QName(tags['tnsa'], option))
        opt_list = document.findall(f'.//{tag}')
        if len(opt_list) == 0:
            print(f"NI MA {tag}")
            newOption = SubElement(ewidencja[0], tag)
            for sub_opt in options[option]:
                sub_tag = str(QName(tags['tnsa'], sub_opt))
                sub_elem = SubElement(newOption, sub_tag)
                sub_elem.text = "0"
                print(sub_elem.tag, sub_elem.text)
    return 0


document = ElementTree.parse('test.XML')
root = document.getroot()
updateOsobaFizyczna(root)
status = updateZakupySprzedaze(root)

if status == 1:
    print("Nie udała sie przemiana")

with open('test_output.xml', 'w') as output_file:
    output_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    output_file.write(ElementTree.tostring(root, encoding='utf-8').decode())
    # output_file.write(prettify(root))



