ANTIBIOTICO_COL_MAP = {
    "Amicacina": "amicacina",
    "Ampicilina": "ampicilina",
    "Amoxicilina-Clavulanato": "amoxicilina_clavulanato",
    "Cefepima": "cefepime",
    "Ceftazidima": "ceftazidime",
    "Ceftriaxona": "ceftriaxone",
    "Cefuroxima": "cefuroxime",
    "Ciprofloxacina": "ciprofloxacino",
    "Ertapenem": "ertapenem",
    "Gentamicina": "gentamicina",
    "Imipenem": "imipenem",
    "Levofloxacina": "levofloxacino",
    "Meropenem": "meropenem",
    "Piperacilina-Tazobactam": "piperacilina_tazobactam",
    "Trimetoprim-Sulfametoxazol": "trimetoprim_sulfametoxazol",
    "Vancomicina": "vancomicina",
    "Tigeciclina": "tigeciclina",
    "Teicoplanina": "teicoplanina",
    "Fluconazol": "fluconazol",
    "Anfotericina B": "anfotericina_b",
}


def apply_antibiogram_to_registry(registry, antibiograma: list):
    for item in antibiograma:
        nome = item.get("nome")
        classificacao = item.get("classificacao")

        coluna = ANTIBIOTICO_COL_MAP.get(nome)
        if coluna:
            setattr(registry, coluna, classificacao)
