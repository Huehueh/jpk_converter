from dataclasses import dataclass
from xml.etree.ElementTree import Element

from namespace import NamespaceHelper

KOD_SYSTEMOWY = "kodSystemowy"
WERSJA_SCHEMY = "wersjaSchemy"
JPK_V7M = "JPK_V7M"
JPK_V7K = "JPK_V7K"




def upgradeV7K(kod_form, kod_form_dekl, wariant_form_dekl):
    kod_form.attrib[KOD_SYSTEMOWY] = "JPK_V7K (2)"
    kod_form.attrib[WERSJA_SCHEMY] = "1-0E"
    if kod_form_dekl is not None:
        kod_form_dekl.attrib[KOD_SYSTEMOWY] = "VAT-7 (16)"
        kod_form_dekl.attrib[WERSJA_SCHEMY] = "1-0E" # TODO: check
        wariant_form_dekl.text = '16'


def upgradeV7M(kod_form, kod_form_dekl, wariant_form_dekl):
    kod_form.attrib[KOD_SYSTEMOWY] = "JPK_V7M (2)"
    # TODO: check  WERSJA_SCHEMY
    if kod_form_dekl is not None:
        kod_form_dekl.attrib[KOD_SYSTEMOWY] = "VAT-7 (22)"
        kod_form_dekl.attrib[WERSJA_SCHEMY] = "1-0E" # TODO: check
        wariant_form_dekl.text = '22'


def upgradeTo2022(document: Element, helper: NamespaceHelper):
    # czesc ewidencyjna
    kod_form = helper.findTnsaElementWithTag('KodFormularza', document)
    kod_form_dekl = helper.findTnsaElementWithTag('KodFormularzaDekl', document)
    wariant_form_dekl = helper.findTnsaElementWithTag('WariantFormularzaDekl', document)
    wariant_form = helper.findTnsaElementWithTag('WariantFormularza', document)

    if kod_form.attrib[KOD_SYSTEMOWY] == "JPK_V7M (1)":
        upgradeV7M(kod_form, kod_form_dekl, wariant_form_dekl)
    elif kod_form.attrib[KOD_SYSTEMOWY] == "JPK_V7K (1)":
        upgradeV7K(kod_form, kod_form_dekl, wariant_form_dekl)

    wariant_form.text = '2'
