from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from utils import getTnsaTag, findTnsaElementWithTag, createTnsaSubElement, changeTagOsFizToEtd, registerNamespaces
import codecs

def updateOsobaFizyczna(document : Element) -> bool:
    os_fiz = findTnsaElementWithTag('OsobaFizyczna', document)
    if os_fiz is None:
        print("W dokumencie nie ma pola 'Osoba fizyczna'")
        return False

    names_to_change = ['NIP', 'ImiePierwsze', 'Nazwisko', 'DataUrodzenia']
    tags_to_change = [getTnsaTag(name, True) for name in names_to_change]

    for element in os_fiz:
        if element.tag in tags_to_change:
            # print(f"Zmieniam {element.tag} na", end=' ')
            element.tag = changeTagOsFizToEtd(element.tag)
            # print(element.tag)
    return True

def updateZakupySprzedaze(document : Element, os_fiz : bool):
    options = {'SprzedazCtrl' : ['LiczbaWierszySprzedazy', 'PodatekNalezny'],
               'ZakupCtrl' : ['LiczbaWierszyZakupow', 'PodatekNaliczony']}

    section = 'Ewidencja'

    pole_ewidencja = findTnsaElementWithTag(section, document)
    if pole_ewidencja is None:
        pole_ewidencja = createTnsaSubElement(section, os_fiz, document)
    for option in options.keys():
        element = findTnsaElementWithTag(option, document)
        if element is None:
            tag = getTnsaTag(option, os_fiz)
            # print(f"Dodaję pole {tag} w polu Ewidencja")
            new_element = SubElement(pole_ewidencja, tag)
            for subelem_title in options[option]:
                subelem = createTnsaSubElement(subelem_title, os_fiz, new_element)
                subelem.text = "0"

def saveFile(root: Element, output_filename : str):
    with open(output_filename, 'wb') as output_file:
        tree = ElementTree.ElementTree(root)
        tree.write(output_file, xml_declaration=False, encoding='utf-8')
        print(f"Wynik konwersji zapisano do {output_filename}")

def convert_file(input_filename : str, output_filename : str):
    registerNamespaces()

    document = ElementTree.parse(input_filename)
    root = document.getroot()
    os_fiz = updateOsobaFizyczna(root)
    updateZakupySprzedaze(root, os_fiz)
    saveFile(root, output_filename)
