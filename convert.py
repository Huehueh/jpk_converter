import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from namespace import NamespaceHelper, tags, tags_v2, tags_v2k, tags_v3k, tags_v3m
from upgrader import upgrade


def updateOsobaFizyczna(helper: NamespaceHelper, document: Element) -> bool:
    os_fiz = helper.findTnsaElementWithTag("OsobaFizyczna", document)
    if os_fiz is None:
        print("W dokumencie nie ma pola 'Osoba fizyczna'")
        return False

    names_to_change = ["NIP", "ImiePierwsze", "Nazwisko", "DataUrodzenia"]
    tags_to_change = [helper.getTnsaTag(name, True) for name in names_to_change]

    for element in os_fiz:
        if element.tag in tags_to_change:
            print(f"Zmieniam {element.tag} na namespace os.fiz", end=" ")
            element.tag = helper.changeTagOsFizToEtd(element.tag)
            print("Wynik", element.tag)
    return True


def updateZakupySprzedaze(helper: NamespaceHelper, document: Element, os_fiz: bool):
    options = {
        "SprzedazCtrl": ["LiczbaWierszySprzedazy", "PodatekNalezny"],
        "ZakupCtrl": ["LiczbaWierszyZakupow", "PodatekNaliczony"],
    }

    section = "Ewidencja"
    pole_ewidencja = helper.findTnsaElementWithTag(section, document)
    if pole_ewidencja is None:
        pole_ewidencja = helper.createTnsaSubElement(
            section, os_fiz, document
        )  # PROBLEM
    for option in options.keys():
        element = helper.findTnsaElementWithTag(option, document)
        if element is None:
            tag = helper.getTnsaTag(option, os_fiz)
            print(f"Dodaję pole {tag} w polu Ewidencja")
            new_element = SubElement(pole_ewidencja, tag)
            for subelem_title in options[option]:
                subelem = helper.createTnsaSubElement(
                    subelem_title, os_fiz, new_element
                )
                subelem.text = "0"


def addPouczenia(helper: NamespaceHelper, document: Element, os_fiz: bool):
    section = "Deklaracja"
    pole_deklaracja = helper.findTnsaElementWithTag(section, document)
    if pole_deklaracja:
        pouczenia = "Pouczenia"
        pole_pouczenia = helper.findTnsaElementWithTag(pouczenia, pole_deklaracja)
        if pole_pouczenia is None:
            pouczenia_value = "1"
            subelem = helper.createTnsaSubElement(pouczenia, True, pole_deklaracja)
            subelem.text = pouczenia_value


def updateVersionIfNeeded(helper: NamespaceHelper, document: Element):
    rok = helper.findTnsaElementWithTag("Rok", document).text
    miesiac = helper.findTnsaElementWithTag("Miesiac", document).text
    print("Rok", rok)
    if int(rok) < 2022:
        print("Konwersja do nowszej wersji niepotrzebna")
        return 1
    elif int(rok) > 2026 or (int(rok) == 2026 and int(miesiac) < 2):
        wersja = 2
    else:
        wersja = 3
    upgrade(document, helper, wersja)
    return wersja
    # zmiana namespace -> w innym miejscu


def saveFile(root: Element, output_filename: str):
    print("Saving", output_filename)
    with open(output_filename, "wb") as output_file:
        tree = ElementTree.ElementTree(root)
        tree.write(output_file, xml_declaration=False, encoding="utf-8")
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


def convert_and_save_file(input_filename: str, output_filename: str):
    try:
        document = ElementTree.parse(input_filename)
    except ElementTree.ParseError as e:
        raise ConversionException from e
    root = document.getroot()
    helper = NamespaceHelper()

    rok = helper.findTnsaElementWithTag("Rok", document).text
    miesiac = helper.findTnsaElementWithTag("Miesiac", document).text
    nip = helper.findTnsaElementWithTag("NIP", document).text

    print("Rok ")

    os_fiz = updateOsobaFizyczna(helper, root)
    updateZakupySprzedaze(helper, root, True)
    addPouczenia(helper, root, os_fiz)
    wersja = updateVersionIfNeeded(helper, root)
    print("UPGRADE WAS NEEDED - > version", wersja)
    if wersja > 1:
        saveFile(root, "temp.xml")
        # zmiana namespace
        upgradeNamespace("temp.xml", output_filename, wersja)
        os.remove("temp.xml")
    else:
        saveFile(root, output_filename)
    print("OUTPUT", output_filename)


def upgradeNamespace(input_xml, output_xml, wersja):
    with open(input_xml, "rb") as infile, open(output_xml, "wb") as outfile:
        data = infile.read()
        for key in tags.keys():
            if wersja == 2:
                if data.find(str.encode("JPK_V7K (2)")) > -1:
                    data = data.replace(
                        str.encode(tags[key]), str.encode(tags_v2k[key])
                    )
                else:
                    data = data.replace(str.encode(tags[key]), str.encode(tags_v2[key]))
            elif wersja == 3:
                if data.find(str.encode("JPK_V7K (3)")) > -1:
                    data = data.replace(
                        str.encode(tags[key]), str.encode(tags_v3k[key])
                    )
                else:
                    data = data.replace(
                        str.encode(tags[key]), str.encode(tags_v3m[key])
                    )

        outfile.write(data)


class ConversionException(Exception):
    pass
