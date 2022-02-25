

from dataclasses import dataclass
from xml.etree.ElementTree import Element

from namespace import NamespaceHelper

KOD_SYSTEMOWY = "kodSystemowy"
WERSJA_SCHEMY = "wersjaSchemy"
JPK_V7M = "JPK_V7M"
JPK_V7K = "JPK_V7K"


def upgradeTo2022(document: Element, helper: NamespaceHelper):
     # czesc ewidencyjna
    pole_kod_form = helper.findTnsaElementWithTag('KodFormularza', document)
    if pole_kod_form.attrib[KOD_SYSTEMOWY] ==  "JPK_V7M (1)":
        pole_kod_form.attrib[KOD_SYSTEMOWY] = "JPK_V7M (2)"
    elif pole_kod_form.attrib[KOD_SYSTEMOWY] ==  "JPK_V7K (1)":
        pole_kod_form.attrib[KOD_SYSTEMOWY] = "JPK_V7K (2)"
    pole_kod_form.attrib[WERSJA_SCHEMY] = "1-0E"

    pole_wariant_form =  helper.findTnsaElementWithTag('WariantFormularza', document)
    pole_wariant_form.text = '2'

    pole_kod_form_dekl =  helper.findTnsaElementWithTag('KodFormularzaDekl', document)
    if pole_kod_form_dekl is not None:
        pole_kod_form_dekl.attrib[KOD_SYSTEMOWY] = "VAT-7 (22)"
        pole_kod_form_dekl.attrib[WERSJA_SCHEMY] = "1-0E"

    pole_wariant_form =  helper.findTnsaElementWithTag('WariantFormularzaDekl', document)
    if pole_wariant_form is not None:
        pole_wariant_form.text = '22'