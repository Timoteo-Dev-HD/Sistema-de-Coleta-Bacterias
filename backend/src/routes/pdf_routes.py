from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback

from src.utils.util import parse_pdf, save_file, parse_date 
from src.utils.util import parse_pdf_procedimentos_anti
from src.utils.util import apply_antibiogram_to_registry
from src.settings.extensions import db
from src.models.registry_model import Registry


pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/pdf/upload", methods=["POST"])
def upload_pdf():
    try:
        print("➡️ Requisição recebida")

        file = request.files.get("file")
        if not file:
            return {"error": "Arquivo não enviado"}, 400

        path = save_file(file)
        print("💾 Arquivo salvo em:", path)

        registros = parse_pdf_procedimentos_anti(path)
        print("📊 Registros extraídos:", len(registros))

        salvos = []
        total = 0
        data_criacao = datetime.now().date()

        for os_item in registros:
            for proc in os_item["procedimentos"]:

                registry = Registry(
                    nome_paciente=os_item["paciente"],
                    local=os_item.get("unidade"),
                    material_coletada=proc.get("material"),
                    microorganismo=proc.get("microorganismo"),
                    data_da_coleta=parse_date(proc.get("data_coleta")),
                    data_admissao=parse_date(proc.get("data_coleta")),
                    data_criacao=data_criacao
                )

                # 👉 AQUI ENTRA O MAPA DE ANTIBIÓTICOS
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
        print("❌ ERRO AO PROCESSAR PDF")
        traceback.print_exc()
        return {"error": str(e)}, 500