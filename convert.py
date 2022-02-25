import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from namespace import NamespaceHelper, tags, tags_v2, tags_v2k
from upgrader import upgradeTo2022


def updateOsobaFizyczna(helper: NamespaceHelper, document : Element) -> bool:
    os_fiz = helper.findTnsaElementWithTag('OsobaFizyczna', document)
    if os_fiz is None:
        print("W dokumencie nie ma pola 'Osoba fizyczna'")
        return False

    names_to_change = ['NIP', 'ImiePierwsze', 'Nazwisko', 'DataUrodzenia']
    tags_to_change = [helper.getTnsaTag(name, True) for name in names_to_change]

    for element in os_fiz:
        if element.tag in tags_to_change:
            print(f"Zmieniam {element.tag} na namespace etd", end=' ')
            element.tag = helper.changeTagOsFizToEtd(element.tag)
            print('Wynik', element.tag)
    return True

def updateZakupySprzedaze(helper: NamespaceHelper, document : Element, os_fiz : bool):
    options = {'SprzedazCtrl' : ['LiczbaWierszySprzedazy', 'PodatekNalezny'],
               'ZakupCtrl' : ['LiczbaWierszyZakupow', 'PodatekNaliczony']}

    section = 'Ewidencja'
    pole_ewidencja = helper.findTnsaElementWithTag(section, document)
    if pole_ewidencja is None:
        pole_ewidencja = helper.createTnsaSubElement(section, os_fiz, document) #PROBLEM
    for option in options.keys():
        element = helper.findTnsaElementWithTag(option, document)
        if element is None:
            tag = helper.getTnsaTag(option, os_fiz)
            print(f"Dodaję pole {tag} w polu Ewidencja")
            new_element = SubElement(pole_ewidencja, tag)
            for subelem_title in options[option]:
                subelem = helper.createTnsaSubElement(subelem_title, os_fiz, new_element)
                subelem.text = "0"

def updateVersionIfNeeded(helper: NamespaceHelper, document: Element):
    rok = helper.findTnsaElementWithTag('Rok', document).text
    print('Rok', rok)
    if int(rok) < 2022:
        print("Konwersja do wersji 2022 niepotrzebna")
        return False

    upgradeTo2022(document, helper)
    # zmiana namespace -> w innym miejscu
    return True

def saveFile(root: Element, output_filename : str):
    print('Saving', output_filename)
    with open(output_filename, 'wb') as output_file:
        tree = ElementTree.ElementTree(root)
        tree.write(output_file, xml_declaration=False, encoding='utf-8')
        print(f"Wynik konwersji zapisano do {output_filename}")


def get_converted_name(name):
    elements = list(os.path.splitext(name))
    elements.insert(len(elements) - 1, "_converted")
    return "".join(elements)

def convert_and_check_xml(input_file: str):
    output_file = get_converted_name(input_file)
    convert_and_save_file(input_file, output_file)
    # from check import is_xml_correct
    # return is_xml_correct(output_file)
    # tymczasem:
    return True



def convert_and_save_file(input_filename : str, output_filename : str):
    try:
        document = ElementTree.parse(input_filename)
    except ElementTree.ParseError as e:
        raise ConversionException from e
    root = document.getroot()
    helper = NamespaceHelper()


    os_fiz = updateOsobaFizyczna(helper, root)
    updateZakupySprzedaze(helper, root, os_fiz)
    upgrade_needed = updateVersionIfNeeded(helper, root)
    print('UPGRADE WAS NEEDED', upgrade_needed)
    if upgrade_needed:
        saveFile(root, 'temp.xml')
        # zmiana namespace
        upgradeNamespace('temp.xml', output_filename)
        os.remove('temp.xml')
    else:
        saveFile(root, output_filename)
    print("OUTPUT", output_filename)



def upgradeNamespace(input_xml, output_xml):
    with open(input_xml, "rb") as infile, open(output_xml, "wb") as outfile:
        data = infile.read()
        for key in tags.keys():
            if data.find(str.encode("JPK_V7K (2)")) > -1:
                data = data.replace(str.encode(tags[key]), str.encode(tags_v2k[key]))
            else:
                data = data.replace(str.encode(tags[key]), str.encode(tags_v2[key]))
        outfile.write(data)


class ConversionException(Exception):
    pass