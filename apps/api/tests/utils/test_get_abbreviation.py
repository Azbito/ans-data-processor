import pytest
from utils.get_abbreviation import get_abbreviation


def test_get_abbreviation():
    assert get_abbreviation("OD") == "Seg. Odontológica"
    assert get_abbreviation("AMB") == "Seg. Ambulatorial"
    assert get_abbreviation("HCO") == "Seg. Hospitalar Com Obstetrícia"
    assert get_abbreviation("HSO") == "Seg. Hospitalar Sem Obstetrícia"
    assert get_abbreviation("REF") == "Plano Referência"
    assert get_abbreviation("PAC") == "Procedimento de Alta Complexidade"
    assert get_abbreviation("DUT") == "Diretriz de Utilização"

    assert get_abbreviation("ABC") == "Abbreviation not found"

    assert get_abbreviation("od") == "Seg. Odontológica"
    assert get_abbreviation("amb") == "Seg. Ambulatorial"

    assert get_abbreviation("hco") == "Seg. Hospitalar Com Obstetrícia"
