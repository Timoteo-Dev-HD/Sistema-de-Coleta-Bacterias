from flask import Blueprint, request, jsonify
from src.utils.util import parse_pdf, save_file, parse_date 
from src.settings.extensions import db
from src.models.registry_model import Registry
import traceback

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

        registros = parse_pdf(path)
        print("📊 Registros extraídos:", len(registros))

        salvos = []

        for item in registros:
            
            #print(item["paciente"])
            
            registry = Registry(
                nome_paciente=item["paciente"],
                data_admissao=parse_date(item["data_admissao"]),
                data_da_coleta=parse_date(item["data_coleta"]),
                data_encerramento=parse_date(item["data_ence"]),
                tempo_coletar=item["tempo_colet"],
                diagnostico=item["diagnostico"],
                desfecho=item["desfecho"]
            )

            db.session.add(registry)
            salvos.append(registry)

        db.session.commit()
        print(f"💾 {len(salvos)} registros salvos no banco")

        # opcional: retornar o que foi salvo
        return jsonify({"salvos": len(salvos)}), 201

    except Exception as e:
        db.session.rollback()
        print("❌ ERRO AO PROCESSAR PDF")
        traceback.print_exc()
        return {"error": str(e)}, 500