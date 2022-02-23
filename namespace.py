from xml.etree.ElementTree import QName, SubElement, Element,register_namespace
import re


tags = {'os_fiz': 'http://crd.gov.pl/wzor/2020/05/08/9394/',
        'os_niefiz': 'http://crd.gov.pl/wzor/2020/05/08/9393/',
        'etd': 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2020/03/11/eD/DefinicjeTypy/'}
tags_v2 = {'os_fiz': 'http://crd.gov.pl/wzor/2021/12/27/11148/',
        'os_niefiz': 'http://crd.gov.pl/wzor/2021/12/27/11148/',
        'etd': 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2021/06/08/eD/DefinicjeTypy/'}
tags_v2k = {'os_fiz': 'http://crd.gov.pl/wzor/2021/12/27/11149/',
        'os_niefiz': 'http://crd.gov.pl/wzor/2021/12/27/11149/',
        'etd': 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2021/06/08/eD/DefinicjeTypy/'}


class NamespaceHelper:
    def __init__(self, year: int = 2022) -> None:
        self.year = year
        self.tags = tags
        self.registerNamespaces()

    def registerNamespaces(self):
        for key, value in tags.items():
            register_namespace(key, value)
        if self.year >= 2022:
            for key, value in tags_v2.items():
                register_namespace(key, value)
            for key, value in tags_v2k.items():
                register_namespace(key, value)

    def getTnsaTag(self, tag : str, os_fiz : bool):
        return str(QName(tags['os_fiz' if os_fiz else 'os_niefiz'], tag))

    def getTnsaTagV2(self, tag : str, os_fiz : bool):
        return str(QName(tags_v2['os_fiz' if os_fiz else 'os_niefiz'], tag))

    def findTnsaElementWithTag(self, tag : str, document : Element) -> Element:
        for option in [True, False]:
            tnsa_tag = self.getTnsaTag(tag, option)
            print(f"findTnsaElementWithTag {tnsa_tag}")
            list = document.findall(f'.//{tnsa_tag}')
            if len(list) != 0:
                return list[0]
        return None

    def createTnsaSubElement(self, tag: str, os_fiz: bool, parent: Element):
        tnsa_tag = self.getTnsaTag(tag, os_fiz)
        new_element = SubElement(parent, tnsa_tag)
        return new_element

    def changeTagOsFizToEtd(self, tag : str):
        return replace({self.tags['os_fiz']: self.tags['etd']}, tag)

    def changeTagsToV2(self):
        self.tags = tags_v2
        # Todo: update namespaces
        replacement = {tags['os_fiz']: self.tags['etd']}   
        find_replacement = lambda m: replacement[m.group(1)]
        regex = r'({})'.format(r'|'.join(re.escape(w) for w in replacement))
        return re.sub(regex, find_replacement, tag)


def replace(replacement_dict: dict, tag: str):
    find_replacement = lambda m: replacement_dict[m.group(1)]
    regex = r'({})'.format(r'|'.join(re.escape(w) for w in replacement_dict))
    return re.sub(regex, find_replacement, tag)