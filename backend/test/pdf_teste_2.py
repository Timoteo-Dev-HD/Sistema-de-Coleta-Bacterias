# from PyPDF2 import PdfReader

# reader = PdfReader("/home/rafael/Projetos/Sistema-de-Coleta-Bacterias/uploads/Hospital_HSLZ-HSE_-_29.12.2025.pdf")

# text1 = reader.pages[21].extract_text()
# text2 = reader.pages[22].extract_text()

# for Indexpage in range(len(reader.pages)):
    
#     print(f"Número da página: {Indexpage+1}\n")
#     print(reader.pages[Indexpage].extract_text())
#     print(f"\n=============================\n")

import re
from PyPDF2 import PdfReader
from pprint import pprint


# ======================================================
# 1. LER TODO O PDF
# ======================================================

reader = PdfReader(
    "/home/rafael/Projetos/Sistema-de-Coleta-Bacterias/uploads/Hospital_HSLZ-HSE_-_29.12.2025.pdf"
)

texto_completo = ""
for page in reader.pages:
    t = page.extract_text()
    if t:
        texto_completo += "\n" + t


# ======================================================
# 2. NORMALIZAR TEXTO
# ======================================================

def normalizar(texto):
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

texto_completo = normalizar(texto_completo)


# ======================================================
# 3. SEPARAR PACIENTES (O.S.:)
# ======================================================

blocos_pacientes = re.split(r"(?=O\.S\.:)", texto_completo)


# ======================================================
# 4. FUNÇÕES AUXILIARES
# ======================================================

def extrair(padrao, texto):
    m = re.search(padrao, texto)
    return m.group(1).strip() if m else None


def extrair_material_completo(texto_proc):
    """
    Captura TODO o bloco do material:
    de 'Material:' até antes de outro Procedimento ou outro O.S.
    """
    material = re.search(
        r"Material:\s*(.*?)"
        r"(?=Procedimento:|O\.S\.:|$)",
        texto_proc,
        re.DOTALL
    )

    return {
        "procedimento": extrair(r"Procedimento:\s*([^\-]+)", texto_proc),
        "material_completo": material.group(1).strip() if material else None
    }


# ======================================================
# 5. PARSE DOS PACIENTES
# ======================================================

pacientes = []

for bloco in blocos_pacientes:
    if not bloco.startswith("O.S.:"):
        continue

    paciente = {
        "os": extrair(r"O\.S\.\:\s*([^\s]+)", bloco),
        "nome": extrair(r"Paciente:\s*([A-ZÀ-Ú\s]+)", bloco),
        "sexo": extrair(r"Sexo:\s*(Masculino|Feminino)", bloco),
        "idade": extrair(r"Idade:\s*(\d+)\s*anos", bloco),
        "data_nascimento": extrair(r"Data nasc\.\:\s*([\d/]+)", bloco),
        "unidade": extrair(r"Unidade coleta:\s*(.*?)\s*Telefone", bloco),
        "materiais": []
    }

    # ==================================================
    # 6. PROCEDIMENTOS / MATERIAIS (N)
    # ==================================================

    blocos_proc = re.split(r"(?=Procedimento:)", bloco)

    for proc in blocos_proc[1:]:
        paciente["materiais"].append(extrair_material_completo(proc))

    pacientes.append(paciente)


# ======================================================
# 7. VISUALIZAR TUDO COMO DICT
# ======================================================

for p in pacientes:
    print("\n" + "=" * 120)
    pprint(p)
