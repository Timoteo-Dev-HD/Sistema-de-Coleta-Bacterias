from flask import current_app
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import re
import pypdf
from datetime import datetime

load_dotenv()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in os.getenv("ALLOWED_EXTENSIONS")

def save_file(file):
    filename = secure_filename(file.filename)
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    return path

def extract_full_text(pdf_path: str) -> str:
    reader = pypdf.PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def split_by_os(text: str):
    blocks = re.split(r'(?=O\.S\.:)', text)
    return blocks

def extract_patient_data(block: str):
    def find(pattern):
        m = re.search(pattern, block)
        return m.group(1).strip() if m else None

    return {
        "os": find(r"O\.S\.: ([\d\-]+)"),
        "paciente": find(r"Paciente:\s*(.+)"),
        "sexo": find(r"Sexo: (\w+)"),
        "idade": find(r"Idade: (\d+)"),
        "data_nasc": find(r"Data nasc\.: ([\d/]+)"),
        "unidade": find(r"Unidade coleta: ([^\n]+)")
    }

def extract_procedimentos(block: str):
    procedimentos = []

    chunks = re.split(r"Procedimento:", block)[1:]

    for chunk in chunks:
        proc = {
            "nome": chunk.split("\n")[0].strip(),
            "status": re.search(r"Status: ([^\n]+)", chunk),
            "material": re.search(r"Material: ([^\n]+)", chunk),
            "data_coleta": re.search(r"Data coleta: ([\d/: ]+)", chunk),
            "resultado": re.search(r"Resultado: ([^\n]+)", chunk)
        }

        procedimentos.append({
            k: v.group(1).strip() if v else None
            for k, v in proc.items()
        })

    return procedimentos




def parse_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        try:
            return datetime.strptime(value, "%d/%m/%Y %H:%M:%S").date()
        except ValueError:
            return None


def parse_pdf(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # quebra por paciente (cada O.S.)
    blocks = re.split(r'\n(?=O\.S\.:)', full_text)

    registros = []

    for block in blocks:
        def find(pattern):
            m = re.search(pattern, block)
            return m.group(1).strip() if m else None

        paciente = find(r"Paciente:\s*([A-Z\s]+)")
        data_nasc = find(r"Data nasc\.: ([\d/]+)")
        data_admissao = find(r"O\.S\.:.*?Data:\s*([\d/]+)")
        data_coleta = find(r"Data coleta:\s*([\d/]+\s*[\d:]+)")
        diagnostico = find(r"Resultado:\s*([^\n]+)")

        if paciente:
            registros.append({
                "paciente": paciente,
                "data_nasc": data_nasc,
                "data_admissao": data_admissao,
                "data_coleta": data_coleta,
                "data_ence": None,          # não existe no PDF
                "tempo_colet": None,        # pode calcular depois
                "diagnostico": diagnostico,
                "desfecho": diagnostico     # por enquanto igual
            })

    return registros



import re
from pypdf import PdfReader

ANTIBIOTIC_REGEX = re.compile(
    r"^([A-Za-zÀ-ÿ\-\/]+)\s+(Sensível|Resistente|Intermediário|Não)\s+(.+)$"
)

def parse_pdf_procedimentos_anti(pdf_path):
    reader = PdfReader(pdf_path)

    registros = []
    current_os = None
    current_proc = None
    current_micro = None

    for page in reader.pages:
        text = page.extract_text()
        if not text:
            continue

        lines = [l.strip() for l in text.split("\n") if l.strip()]

        for line in lines:

            # 🔹 NOVA O.S.
            if line.startswith("O.S.:"):
                current_os = {
                    "procedimentos": []
                }
                registros.append(current_os)

                current_proc = None
                current_micro = None

                current_os["os"] = re.search(r"O\.S\.\:\s*([^\s]+)", line).group(1)
                current_os["paciente"] = re.search(r"Paciente:\s*(.+)", line).group(1)

            # 🔹 Dados do paciente
            elif line.startswith("Sexo:") and current_os:
                current_os["sexo"] = "Feminino" if "Feminino" in line else "Masculino"

            elif line.startswith("Unidade coleta:") and current_os:
                current_os["unidade"] = line.replace("Unidade coleta:", "").strip()

            # 🔹 NOVO PROCEDIMENTO
            elif line.startswith("Procedimento:") and current_os:
                current_proc = {
                    "antibiograma": []
                }
                current_os["procedimentos"].append(current_proc)

                current_micro = None

                current_proc["procedimento"] = line.replace("Procedimento:", "").strip()

            elif line.startswith("Material:") and current_proc:
                # Exemplo:
                # "Material: Urina de Jato Médio Data coleta: 19/12/2025 18:12:20"
                content = line.replace("Material:", "").strip()

                if "Data coleta:" in content:
                    material, data_coleta = content.split("Data coleta:", 1)
                    current_proc["material"] = material.strip()
                    current_proc["data_coleta"] = data_coleta.strip()
                else:
                    current_proc["material"] = content


            # 🔹 Microrganismo
            elif line.startswith("Grupo: Microrganismos Resultado:") and current_proc:
                current_micro = line.replace(
                    "Grupo: Microrganismos Resultado:", ""
                ).replace("~", "").strip()

                current_proc["microorganismo"] = current_micro

            # 🔹 ANTIBIÓTICOS
            else:
                match = ANTIBIOTIC_REGEX.match(line)
                if match and current_proc and current_micro:
                    current_proc["antibiograma"].append({
                        "antimicrobiano": match.group(1),
                        "classificacao": match.group(2),
                        "mic": match.group(3)
                    })

    return registros




def apply_antibiogram_to_registry(registry, antibiograma):
    """
    antibiograma = [
      {antimicrobiano, classificacao, mic}
    ]
    """

    MAP = {
        "Amicacina": "amicacina",
        "Ampicilina": "ampicilina",
        "Amoxicilina": "amoxicilina",
        "Amoxicilina-Clavulanato": "amoxicilina_clavulanato",
        "Cefalexina": "cefalexina",
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
        "Clindamicina": "clindamicina",
        "Daptomicina": "daptomicina",
        "Eritromicina": "eritromicina",
        "Nitrofurantoina": "nitrofurantoina",
        "Aztreonam": "aztreonam",
        "Ceftazidima-Avibactam": "ceftazidima_avibactam",
    }

    for item in antibiograma:
        coluna = MAP.get(item["antimicrobiano"])
        if coluna:
            # exemplo: "Sensível <=4"
            setattr(
                registry,
                coluna,
                f'{item["classificacao"]} {item["mic"]}'
            )
