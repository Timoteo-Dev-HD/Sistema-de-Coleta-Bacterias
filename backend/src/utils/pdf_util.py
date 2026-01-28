import re
from PyPDF2 import PdfReader


# =====================================================
# NORMALIZA TEXTO
# =====================================================

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()


# =====================================================
# PARSE DO MATERIAL COMPLETO
# =====================================================

def parse_material_completo(material_texto: str) -> dict:
    dados = {}

    # MATERIAL
    m_material = re.search(
        r"Material:\s*(.*?)\s*Data coleta:",
        material_texto,
        re.DOTALL
    )
    dados["material"] = m_material.group(1).strip() if m_material else None

    # DATA COLETA
    m_data = re.search(r"Data coleta:\s*([\d/]+)", material_texto)
    dados["data_coleta"] = m_data.group(1) if m_data else None

    # MICRORGANISMO (PARA NO PRÓXIMO BLOCO)
    m_micro = re.search(
        r"Resultado:\s*(.*?)\s*(?:Antimicrobiano|Observações do isolado:)",
        material_texto,
        re.DOTALL
    )
    dados["microorganismo"] = (
        m_micro.group(1).replace("~", "").strip()
        if m_micro else None
    )

    # OBSERVAÇÃO (LIMITADA AO BLOCO)
    m_obs = re.search(
        r"Observações do isolado:\s*(.*?)(?:Procedimento:|O\.S\.:|$)",
        material_texto,
        re.DOTALL
    )
    dados["observacao"] = (
        m_obs.group(1).strip()
        if m_obs else None
    )

    # ANTIBIOGRAMA
    bloco = re.search(
        r"Antimicrobiano\s*(.*?)\s*(?:Observações do isolado:|$)",
        material_texto,
        re.DOTALL
    )

    antibiograma = []

    if bloco:
        bloco = bloco.group(1)

        nomes = re.findall(
            r"(Amicacina|Amoxicilina-Clavulanato \(f\)|Ampicilina|Cefepima|"
            r"Ceftazidima|Ceftriaxona|Cefuroxima|Ciprofloxacina|Ertapenem|"
            r"Gentamicina|Imipenem|Levofloxacina|Meropenem|"
            r"Piperacilina-Tazobactam|Trimetoprim-Sulfametoxazol|"
            r"Ceftazidima-Avibactam|Vancomicina|Tigeciclina|Teicoplanina|"
            r"Fluconazol|Anfotericina B)",
            bloco
        )

        classificacoes = re.findall(
            r"(Sensível|Resistente|Intermediário|Não definido)",
            bloco
        )

        mics = re.findall(
            r"(<=|>=|<|>)?\s*[\d.,/]+",
            bloco
        )

        for i, nome in enumerate(nomes):
            antibiograma.append({
                "nome": nome.replace(" (f)", ""),
                "classificacao": classificacoes[i] if i < len(classificacoes) else None,
                "mic": mics[i] if i < len(mics) else None
            })

    dados["antibiograma"] = antibiograma
    return dados



# =====================================================
# PARSE DO PDF COMPLETO
# =====================================================

def parse_pdf_procedimentos_anti(path: str) -> list:
    reader = PdfReader(path)

    texto = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            texto += "\n" + t

    texto = normalize(texto)
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
            m_material = re.search(
                r"Material:\s*(.*?)\s*(?=Procedimento:|O\.S\.:|$)",
                proc,
                re.DOTALL
            )
            if m_material:
                item["procedimentos"].append(
                    parse_material_completo(m_material.group(1))
                )

        registros.append(item)

    return registros
