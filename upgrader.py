from dataclasses import dataclass
from xml.etree.ElementTree import Element

from namespace import NamespaceHelper

KOD_SYSTEMOWY = "kodSystemowy"
WERSJA_SCHEMY = "wersjaSchemy"


def upgradeV7K(kod_form, kod_form_dekl, wariant_form_dekl, wersja):
    kod_form.attrib[KOD_SYSTEMOWY] = f"JPK_V7K ({wersja})"
    kod_form.attrib[WERSJA_SCHEMY] = "1-0E"
    if kod_form_dekl is not None:
        wariant = 16 if wersja == 2 else 17
        kod_form_dekl.attrib[KOD_SYSTEMOWY] = f"VAT-7K ({wariant})"
        kod_form_dekl.attrib[WERSJA_SCHEMY] = "1-0E"
        wariant_form_dekl.text = f"{wariant}"


def upgradeV7M(kod_form, kod_form_dekl, wariant_form_dekl, wersja):
    kod_form.attrib[KOD_SYSTEMOWY] = "JPK_V7M (2)"
    # TODO: check  WERSJA_SCHEMY
    if kod_form_dekl is not None:
        wariant = 22 if wersja == 2 else 23
        kod_form_dekl.attrib[KOD_SYSTEMOWY] = f"VAT-7 ({wariant})"
        kod_form_dekl.attrib[WERSJA_SCHEMY] = "1-0E"
        wariant_form_dekl.text = f"{wariant}"


def upgrade(document: Element, helper: NamespaceHelper, wersja):
    # czesc ewidencyjna
    kod_form = helper.findTnsaElementWithTag("KodFormularza", document)
    kod_form_dekl = helper.findTnsaElementWithTag("KodFormularzaDekl", document)
    wariant_form_dekl = helper.findTnsaElementWithTag("WariantFormularzaDekl", document)
    wariant_form = helper.findTnsaElementWithTag("WariantFormularza", document)

    wariant_form.text = f"{wersja}"
    if kod_form.attrib[KOD_SYSTEMOWY].startswith("JPK_V7M"):
        upgradeV7M(kod_form, kod_form_dekl, wariant_form_dekl, wersja)
    elif kod_form.attrib[KOD_SYSTEMOWY].startswith("JPK_V7K"):
        upgradeV7K(kod_form, kod_form_dekl, wariant_form_dekl, wersja)
