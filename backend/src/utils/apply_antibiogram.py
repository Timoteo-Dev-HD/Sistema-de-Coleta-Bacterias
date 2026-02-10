ANTIBIOTICO_COL_MAP = {
    # Aminoglicosídeos
    "Amicacina": "amicacina",
    "Gentamicina": "gentamicina",
    "Estreptomicina": "streptomicina",

    # Penicilinas
    "Ampicilina": "ampicilina",
    "Amoxicilina": "amoxicilina",
    "Penicilina": "penicilina",
    "Oxacilina": "oxacilina",

    # Associações com inibidor
    "Amoxicilina-Clavulanato": "amoxicilina_clavulanato",
    "Ampicilina-Sulbactam": "amp_sulbactam",
    "Piperacilina-Tazobactam": "piperacilina_tazobactam",

    # Cefalosporinas
    "Cefalexina": "cefalexina",
    "Cefazolina": "cefazolina",
    "Cefepima": "cefepime",
    "Ceftazidima": "ceftazidime",
    "Cefoxitina": "cefoxitina",
    "Ceftriaxona": "ceftriaxone",
    "Cefuroxima": "cefuroxime",
    "Cefotaxime": "cefotaxime",
    "Ceftibufen": "ceftibufen",
    "Ceftarolina": "ceftarolina",

    # Carbapenêmicos
    "Imipenem": "imipenem",
    "Meropenem": "meropenem",
    "Ertapenem": "ertapenem",

    # Fluoroquinolonas
    "Ciprofloxacina": "ciprofloxacino",
    "Levofloxacina": "levofloxacino",
    "Moxifloxacina": "moxifloxacina",
    "Ofloxacina": "ofloxacina",
    "Norfloxacina": "norfloxacina",

    # Macrolídeos / Lincosamidas
    "Eritromicina": "eritromicina",
    "Azitromicina": "azitromicina",
    "Clindamicina": "clindamicina",

    # Glicopeptídeos / Oxazolidinonas
    "Vancomicina": "vancomicina",
    "Teicoplanina": "teicoplanina",
    "Linezolida": "linezolida",

    # Outros antibacterianos
    "Daptomicina": "daptomicina",
    "Tigeciclina": "tigeciclina",
    "Minociclina": "minociclina",
    "Tetraciclina": "tetraciclina",
    "Rifampicina": "rifampicina",
    "Colistina": "colistina",
    "Polimixina B": "polimixina_b",
    "Cloranfenicol": "cloranfenicol",
    "Aztreonam": "aztreonam",
    "Nitrofurantoina": "nitrofurantoina",
    "Trimetoprim-Sulfametoxazol": "trimetoprim_sulfametoxazol",

    # Betalactâmicos especiais
    "Ceftazidima-Avibactam": "ceftazidima_avibactam",
    "Ceftolozano-Tazobactam": "ceftolozano_tazobactam",

    # Antifúngicos
    "Anfotericina B": "anfotericina_b",
    "Fluconazol": "fluconazol",
    "Ketoconazol": "ketoconazol",
    "Voriconazol": "voriconazol",
    "Nazol": "nazol",
}


def apply_antibiogram_to_registry(registry, antibiograma: list):
    for item in antibiograma:
        nome = item.get("nome")
        classificacao = item.get("classificacao")
        mic = item.get("mic")

        coluna = ANTIBIOTICO_COL_MAP.get(nome)
        if coluna:
                # exemplo salvo: "Sensível <=4"
                valor = classificacao
                if mic:
                    valor = f"{classificacao}"

                setattr(registry, coluna, valor)