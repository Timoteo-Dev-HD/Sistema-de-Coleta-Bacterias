import re
from PyPDF2 import PdfReader


def parse_pdf_procedimentos_anti(path: str) -> list:
    reader = PdfReader(path)

    texto = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            texto += "\n" + t

    texto = re.sub(r"\s+", " ", texto)

    blocos = re.split(r"(?=O\.S\.:)", texto)
    registros = []

    for bloco in blocos:
        if not bloco.startswith("O.S.:"):
            continue

        paciente = re.search(r"Paciente:\s*([A-ZÀ-Ú\s]+)", bloco)
        unidade = re.search(r"Unidade coleta:\s*(.*?)\s*Telefone", bloco)

        item = {
            "paciente": paciente.group(1).strip() if paciente else None,
            "unidade": unidade.group(1).strip() if unidade else None,
            "procedimentos": []
        }

        procedimentos = re.split(r"(?=Procedimento:)", bloco)

        for proc in procedimentos[1:]:
            item["procedimentos"].append(
                extrair_material_antibiograma(proc)
            )

        registros.append(item)

    return registros

def extrair_material_antibiograma(texto_proc: str) -> dict:
    material = re.search(
        r"Material:\s*(.*?)\s*Data coleta",
        texto_proc
    )

    data = re.search(
        r"Data coleta:\s*([\d/]+)",
        texto_proc
    )

    micro = re.search(
        r"Resultado:\s*([A-Za-zÀ-ú\s~\.]+?)\s*Antimicrobiano",
        texto_proc
    )

    obs = re.search(
        r"Observações do isolado:\s*(.+)",
        texto_proc
    )

    antibiograma = []

    for nome, classif in re.findall(
        r"(Amicacina|Ampicilina|Amoxicilina-Clavulanato|Aztreonam|Cefepima|Ceftazidima|Ceftriaxona|Cefuroxima|Ciprofloxacina|Ertapenem|Gentamicina|Imipenem|Levofloxacina|Meropenem|Norfloxacina|Piperacilina-Tazobactam|Polimixina B|Trimetoprim-Sulfametoxazol|Vancomicina|Linezolid|Tigeciclina|Teicoplanina|Fluconazol|Anfotericina B)\s+(Sensível|Resistente|Intermediário|Não definido)",
        texto_proc,
        re.IGNORECASE
    ):
        antibiograma.append({
            "nome": nome,
            "classificacao": classif
        })

    return {
        "material": material.group(1).strip() if material else None,
        "data_coleta": data.group(1) if data else None,
        "microorganismo": micro.group(1).replace("~", "").strip() if micro else None,
        "observacao": obs.group(1).strip() if obs else None,
        "antibiograma": antibiograma
    }

ANTIBIOTICO_COL_MAP = {
    "Amicacina": "amicacina",
    "Ampicilina": "ampicilina",
    "Amoxicilina-Clavulanato": "amoxicilina_clavulanato",
    "Aztreonam": "aztreonam",
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
    "Norfloxacina": "norfloxacina",
    "Piperacilina-Tazobactam": "piperacilina_tazobactam",
    "Polimixina B": "polimixina_b",
    "Trimetoprim-Sulfametoxazol": "trimetoprim_sulfametoxazol",
    "Vancomicina": "vancomicina",
    "Linezolid": "linezolida",
    "Tigeciclina": "tigeciclina",
    "Teicoplanina": "teicoplanina",
    "Fluconazol": "fluconazol",
    "Anfotericina B": "anfotericina_b",
}


def apply_antibiogram_to_registry(registry, antibiograma: list):
    for item in antibiograma:

        # CASO 1: dict com chave "nome"
        if isinstance(item, dict) and "nome" in item:
            nome = item["nome"]
            classificacao = item.get("classificacao")

        # CASO 2: dict { "Amicacina": "Sensível" }
        elif isinstance(item, dict) and len(item) == 1:
            nome, classificacao = next(iter(item.items()))

        # CASO 3: tupla ("Amicacina", "Sensível")
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            nome, classificacao = item[0], item[1]

        else:
            # formato desconhecido → ignora
            continue

        coluna = ANTIBIOTICO_COL_MAP.get(nome)
        if coluna:
            setattr(registry, coluna, classificacao)
