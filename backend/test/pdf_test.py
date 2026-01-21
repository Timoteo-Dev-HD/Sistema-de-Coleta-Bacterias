from pypdf import PdfReader


# def extract_pdf_data_test(pdf_path):
#     reader = PdfReader(pdf_path)
#     dados = reader.pages[4].extract_text()
#     print(dados)
    
# extract_pdf_data_test("/home/rafael/Projetos/Sistema-de-Coleta-Bacterias/backend/uploads/Hospital_HSLZ-HSE_-_30.12.2025.pdf")






# import re
# from pypdf import PdfReader

# ANTIBIOTIC_REGEX = re.compile(
#     r"^([A-Za-zÀ-ÿ\-\/\s]+)\s+(Sensível|Resistente|Intermediário|Não definido)\s+(.+)$"
# )

# def parse_pdf_full(pdf_path):
#     reader = PdfReader(pdf_path)

#     registros = []
#     current_os = None
#     current_proc = None
#     current_micro = None

#     for page in reader.pages:
#         text = page.extract_text()
#         if not text:
#             continue

#         lines = [l.strip() for l in text.split("\n") if l.strip()]

#         for line in lines:

#             # =========================
#             # NOVA O.S.
#             # =========================
#             if line.startswith("O.S.:"):
#                 current_os = {
#                     "procedimentos": [],
#                     "raw_text": []
#                 }
#                 registros.append(current_os)

#                 current_proc = None
#                 current_micro = None

#                 current_os["os"] = re.search(r"O\.S\.\:\s*([^\s]+)", line).group(1)
#                 current_os["data_os"] = re.search(r"Data:\s*([\d/]+\s[\d:]+)", line).group(1)
#                 current_os["paciente"] = re.search(r"Paciente:\s*(.+)", line).group(1)

#             # =========================
#             # DADOS DO PACIENTE
#             # =========================
#             elif current_os:
#                 current_os["raw_text"].append(line)

#                 if line.startswith("Sexo:"):
#                     current_os["sexo"] = "Feminino" if "Feminino" in line else "Masculino"
#                     idade = re.search(r"Idade:\s*(\d+)", line)
#                     if idade:
#                         current_os["idade"] = idade.group(1)

#                 elif "Data nasc.:" in line:
#                     current_os["data_nascimento"] = line.split("Data nasc.:")[1].strip()

#                 elif line.startswith("Unidade coleta:"):
#                     current_os["unidade"] = line.replace("Unidade coleta:", "").strip()

#                 elif line.startswith("Telefone:"):
#                     current_os["telefone"] = line.replace("Telefone:", "").strip()

#                 elif line.startswith("Endereco do paciente:"):
#                     current_os["endereco"] = line.replace("Endereco do paciente:", "").strip()

#                 elif line.startswith("Fonte Pagadora:"):
#                     current_os["fonte_pagadora"] = line.replace("Fonte Pagadora:", "").strip()

#             # =========================
#             # NOVO PROCEDIMENTO
#             # =========================
#             if line.startswith("Procedimento:") and current_os:
#                 current_proc = {
#                     "microrganismos": [],
#                     "raw_text": []
#                 }
#                 current_os["procedimentos"].append(current_proc)

#                 current_micro = None

#                 current_proc["procedimento"] = line.replace("Procedimento:", "").strip()

#             elif current_proc:
#                 current_proc["raw_text"].append(line)

#                 if line.startswith("Status:"):
#                     current_proc["status"] = line.replace("Status:", "").strip()

#                 elif line.startswith("Material:"):
#                     current_proc["material"] = line.replace("Material:", "").strip()

#                 elif "Data coleta:" in line:
#                     current_proc["data_coleta"] = line.split("Data coleta:")[1].strip()

#             # =========================
#             # MICRORGANISMO
#             # =========================
#             if line.startswith("Grupo: Microrganismos Resultado:") and current_proc:
#                 current_micro = {
#                     "antibiograma": [],
#                     "observacoes": [],
#                     "raw_text": []
#                 }
#                 current_proc["microrganismos"].append(current_micro)

#                 current_micro["nome"] = line.replace(
#                     "Grupo: Microrganismos Resultado:", ""
#                 ).replace("~", "").strip()

#             elif current_micro:
#                 current_micro["raw_text"].append(line)

#                 if line.startswith("Observações do isolado:"):
#                     current_micro["observacoes"].append(
#                         line.replace("Observações do isolado:", "").strip()
#                     )

#                 elif line.startswith("Contagem de colônias:"):
#                     current_micro["contagem_colonias"] = line.replace(
#                         "Contagem de colônias:", ""
#                     ).strip()

#                 else:
#                     match = ANTIBIOTIC_REGEX.match(line)
#                     if match:
#                         current_micro["antibiograma"].append({
#                             "antimicrobiano": match.group(1).strip(),
#                             "classificacao": match.group(2),
#                             "mic": match.group(3)
#                         })

#     return registros



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
                current_proc["material"] = line.replace("Material:", "").strip()

            elif "Data coleta:" in line and current_proc:
                current_proc["data_coleta"] = line.split("Data coleta:")[1].strip()

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

dados = parse_pdf_procedimentos_anti(
    "/home/rafael/Projetos/Sistema-de-Coleta-Bacterias/backend/uploads/Hospital_HSLZ-HSE_-_30.12.2025.pdf"
)

print(dados[4])
