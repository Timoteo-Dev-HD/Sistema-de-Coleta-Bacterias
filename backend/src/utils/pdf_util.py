import re
from PyPDF2 import PdfReader


# =====================================================
# NORMALIZA TEXTO
# =====================================================
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()

# =====================================================
# NOME DE PACIENTE
# =====================================================
def clean_patient_name(nome: str) -> str:
    if not nome:
        return nome

    nome = nome.strip()
    
    nome = re.sub(r"\s+S$", "", nome)
    
    nome = re.sub(r"\s+", " ", nome)
    
    return nome


# =====================================================
# PARSE DO MATERIAL COMPLETO
# =====================================================
def parse_material_completo(material_texto: str) -> dict:
    dados = {}

    # 🔹 MATERIAL (funciona com ou sem Data coleta)
    m_material = re.search(
        r"Material:\s*(.*?)(?:\s*Data coleta:|$)",
        material_texto,
        re.DOTALL
    )
    dados["material"] = m_material.group(1).strip() if m_material else None

    # 🔹 DATA DA COLETA (com ou sem hora)
    m_data = re.search(
        r"Data coleta:\s*([\d/]+(?:\s*[\d:]+)?)",
        material_texto
    )
    dados["data_coleta"] = m_data.group(1).strip() if m_data else None

    # 🔹 MICRORGANISMO
    m_micro = re.search(
        r"Resultado:\s*(.*?)\s*(?:Antimicrobiano|Observações do isolado:)",
        material_texto,
        re.DOTALL
    )
    dados["microorganismo"] = (
        m_micro.group(1).replace("~", "").strip()
        if m_micro else None
    )

    # 🔹 OBSERVAÇÕES
    m_obs = re.search(
        r"Observações do isolado:\s*(.*?)(?:Procedimento:|O\.S\.:|$)",
        material_texto,
        re.DOTALL
    )
    dados["observacao"] = m_obs.group(1).strip() if m_obs else None

    # =================================================
    # 🔹 ANTIBIOGRAMA
    # =================================================
    bloco = re.search(
        r"Antimicrobiano\s*(.*?)\s*(?:Observações do isolado:|$)",
        material_texto,
        re.DOTALL
    )

    antibiograma = []

    if bloco:
        bloco = bloco.group(1)

        nomes = re.findall(
            r"(Amicacina|Ampicilina|Amoxicilina|Amoxicilina-Clavulanato \(f\)|"
            r"Ampicilina-Sulbactam|Azitromicina|Penicilina|Oxacilina|"
            r"Cefalexina|Cefazolina|Cefepima|Cefoxitina|Ceftazidima|"
            r"Ceftriaxona|Cefuroxima|Cefotaxime|Ceftibufen|Ceftarolina|"
            r"Ciprofloxacina|Levofloxacina|Moxifloxacina|Ofloxacina|Norfloxacina|"
            r"Eritromicina|Clindamicina|Linezolida|"
            r"Imipenem|Meropenem|Ertapenem|"
            r"Gentamicina|Estreptomicina|Amicacina|"
            r"Daptomicina|Tigeciclina|Minociclina|Tetraciclina|Rifampicina|"
            r"Polimixina B|Colistina|Cloranfenicol|Aztreonam|Nitrofurantoina|"
            r"Trimetoprim-Sulfametoxazol|"
            r"Piperacilina-Tazobactam|"
            r"Ceftazidima-Avibactam|Ceftolozano-Tazobactam|"
            r"Vancomicina|Teicoplanina|"
            r"Anfotericina B|Fluconazol|Ketoconazol|Voriconazol|Nazol)",
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

    # print("🧪 MATERIAL:", dados["material"])
    # print("🧪 DATA:", dados["data_coleta"])
    # print("🧪 MICRO:", dados["microorganismo"])

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

    # 🔹 Quebra por O.S.
    blocos = re.split(r"(?=O\.S\.:)", texto)

    registros = []

    for bloco in blocos:
        if not bloco.startswith("O.S.:"):
            continue

        paciente_match = re.search(r"Paciente:\s*([A-ZÀ-Ú\s]+)", bloco)

        paciente = (
            clean_patient_name(paciente_match.group(1))
            if paciente_match else None
        )

        data_nasc = re.search(r"Data nasc\.\:\s*([\d/]+)", bloco)
        unidade = re.search(r"Unidade coleta:\s*(.*?)\s*Telefone", bloco)

        item = {
            "paciente": paciente,
            "unidade": unidade.group(1).strip() if unidade else None,
            "data_nascimento": data_nasc.group(1) if data_nasc else None,
            "procedimentos": []
        }

        print("👤 PACIENTE:", item["paciente"])
        # print("🎂 NASC:", item["data_nascimento"])


        # 🔹 Quebra por procedimento
        procedimentos = re.split(r"(?=Procedimento:)", bloco)

        for proc in procedimentos[1:]:
            dados = parse_material_completo(proc)

            # só adiciona se realmente achou material ou micro
            if dados.get("material") or dados.get("microorganismo"):
                item["procedimentos"].append(dados)


        registros.append(item)

    return registros
