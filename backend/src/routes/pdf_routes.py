from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback

from src.utils.pdf_util import parse_pdf_procedimentos_anti
from src.utils.apply_antibiogram import apply_antibiogram_to_registry
from src.utils.util import save_file, parse_date
from src.settings.extensions import db
from src.models.registry_model import Registry

pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/pdf/upload", methods=["POST"])
def upload_pdf():
    try:
        file = request.files.get("file")
        if not file:
            return {"error": "Arquivo não enviado"}, 400

        # 🔹 Salva o PDF
        path = save_file(file)

        # 🔹 Parse completo (PACIENTE → PROCEDIMENTOS → MATERIAL)
        registros = parse_pdf_procedimentos_anti(path)

        hoje = datetime.now().date()
        total = 0

        for paciente in registros:
            for proc in paciente["procedimentos"]:

                registry = Registry(
                    nome_paciente=paciente.get("paciente"),
                    local=paciente.get("unidade"),
                    material_coletada=proc.get("material"),   # ✅ AQUI
                    microorganismo=proc.get("microorganismo"),
                    data_da_coleta=parse_date(proc.get("data_coleta")),
                    data_admissao=parse_date(proc.get("data_coleta")),
                    observacao=proc.get("observacao"),
                    data_criacao=hoje,
                    data_atualizacao=hoje
                )

                # 🔬 Aplica antibiograma
                apply_antibiogram_to_registry(
                    registry,
                    proc.get("antibiograma", [])
                )

                db.session.add(registry)
                total += 1

        db.session.commit()

        return jsonify({
            "status": "ok",
            "registros_salvos": total
        }), 201

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return {"error": str(e)}, 500
