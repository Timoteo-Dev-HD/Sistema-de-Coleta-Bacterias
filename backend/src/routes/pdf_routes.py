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

        path = save_file(file)
        registros = parse_pdf_procedimentos_anti(path)

        total = 0
        hoje = datetime.now().date()

        for os_item in registros:
            for proc in os_item["procedimentos"]:

                # 🔒 proteção de tamanho (mesmo com Text)
                observacao = proc.get("observacao")
                if observacao:
                    observacao = observacao[:5000]

                registry = Registry(
                    nome_paciente=os_item.get("paciente"),
                    local=os_item.get("unidade"),
                    material_coletada=proc.get("material"),
                    microorganismo=proc.get("microorganismo"),
                    data_da_coleta=parse_date(proc.get("data_coleta")),
                    data_admissao=parse_date(proc.get("data_coleta")),
                    observacao=observacao,
                    data_criacao=hoje,
                    data_atualizacao=hoje
                )

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

