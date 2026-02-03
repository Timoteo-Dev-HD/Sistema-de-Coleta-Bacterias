import os
from src.utils.pdf_util import parse_pdf_procedimentos_anti


def test_parse_pdf_real():
    # 📄 Caminho do PDF real
    base_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(base_dir, "fixtures", "exame_exemplo.pdf")

    assert os.path.exists(pdf_path), "PDF de teste não encontrado"

    registros = parse_pdf_procedimentos_anti(pdf_path)

    # 🔹 Deve ter pelo menos 1 paciente
    assert len(registros) > 0

    paciente = registros[0]
    assert paciente["paciente"] is not None
    assert "procedimentos" in paciente
    assert len(paciente["procedimentos"]) > 0

    procedimento = paciente["procedimentos"][0]

    # 🔹 MATERIAL DA COLETA
    assert procedimento.get("material") is not None
    print("🧪 Material:", procedimento["material"])

    # 🔹 DATA COLETA
    assert procedimento.get("data_coleta") is not None
    print("📅 Data coleta:", procedimento["data_coleta"])

    # 🔹 MICROORGANISMO
    assert procedimento.get("microorganismo") is not None
    print("🦠 Microorganismo:", procedimento["microorganismo"])

    # 🔹 ANTIBIOGRAMA
    antibiograma = procedimento.get("antibiograma")
    assert isinstance(antibiograma, list)

    if antibiograma:
        print("💊 Antibióticos encontrados:")
        for a in antibiograma:
            print(
                f" - {a['nome']} | {a['classificacao']} {a['mic']}"
            )
