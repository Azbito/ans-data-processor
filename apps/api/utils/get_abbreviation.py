def get_abbreviation(target: str) -> str:
    mapped_abbreviations = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial",
        "HCO": "Seg. Hospitalar Com Obstetrícia",
        "HSO": "Seg. Hospitalar Sem Obstetrícia",
        "REF": "Plano Referência",
        "PAC": "Procedimento de Alta Complexidade",
        "DUT": "Diretriz de Utilização",
    }

    return mapped_abbreviations.get(target.upper(), "Abbreviation not found")
