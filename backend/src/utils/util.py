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

