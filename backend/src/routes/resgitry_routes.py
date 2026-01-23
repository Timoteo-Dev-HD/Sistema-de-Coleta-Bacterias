from flask import (
    Blueprint,
    request,
    jsonify
)
from datetime import datetime
from sqlalchemy import asc
from src.models.registry_model import Registry
from src.settings.extensions import db

registry_bp = Blueprint("registry", __name__)

@registry_bp.route("/registry", methods=["POST"])
def create_registry():
    pass


@registry_bp.route("/registry", methods=["GET"])
def lista_registry():
    try:
        registros = (
            Registry.query
            .order_by(Registry.nome_paciente)
            .all()
        )

        return jsonify([
            {
                "id": r.id,
                "nome_paciente": r.nome_paciente,
                "data_admissao": r.data_admissao.isoformat() if r.data_admissao else None,
                "data_da_coleta": r.data_da_coleta.isoformat() if r.data_da_coleta else None,
                "data_encerramento": r.data_encerramento.isoformat() if r.data_encerramento else None,
                "tempo_coletar": r.tempo_coletar,
                "diagnostico": r.diagnostico,
                "desfecho": r.desfecho,
                "notificacao": r.notificacao,
                "dialise": r.dialise,
                "material_coletada": r.material_coletada,
                "microorganismo": r.microorganismo,
                "local": r.local,
                "observacao": r.observacao,

                # 🧪 ANTIBIÓTICOS
                "amicacina": r.amicacina,
                "ampicilina": r.ampicilina,
                "amoxicilina": r.amoxicilina,
                "amoxicilina_clavulanato": r.amoxicilina_clavulanato,
                "cefepime": r.cefepime,
                "ceftazidime": r.ceftazidime,
                "ceftriaxone": r.ceftriaxone,
                "cefuroxime": r.cefuroxime,
                "ciprofloxacino": r.ciprofloxacino,
                "ertapenem": r.ertapenem,
                "gentamicina": r.gentamicina,
                "imipenem": r.imipenem,
                "levofloxacino": r.levofloxacino,
                "meropenem": r.meropenem,
                "norfloxacina": r.norfloxacina,
                "piperacilina_tazobactam": r.piperacilina_tazobactam,
                "polimixina_b": r.polimixina_b,
                "trimetoprim_sulfametoxazol": r.trimetoprim_sulfametoxazol,
                "vancomicina": r.vancomicina,
                "nitrofurantoina": r.nitrofurantoina,
                "ceftazidima_avibactam": r.ceftazidima_avibactam,
                "data_criacao": r.data_criacao,
                "data_atulizacao": r.data_atualizacao
            }
            for r in registros
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 50
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@registry_bp.route("/registry/<int:id_registry>", methods=["PUT"])
def update_registry(id_registry):
    data = request.json

    registry = Registry.query.get_or_404(id_registry)

    def parse_date(value):
        if not value:
            return None
        return datetime.strptime(value, "%Y-%m-%d").date()

    registry.data_admissao = parse_date(data.get("data_admissao"))
    registry.data_da_coleta = parse_date(data.get("data_da_coleta"))
    registry.data_encerramento = parse_date(data.get("data_encerramento"))

    registry.diagnostico = data.get("diagnostico") or None
    registry.desfecho = data.get("desfecho") or None
    registry.notificacao = data.get("notificacao") or None
    registry.dialise = data.get("dialise") or None
    registry.local = data.get("local") or None
    registry.observacao = data.get("observacao") or None

    db.session.commit()

    return jsonify({"success": True})


@registry_bp.route("/registry/<int:id_registry>", methods=["DELETE"])
def delete_registry(id_registry):
    try:
        select_registry = db.session.query(Registry).filter(Registry.id == id_registry).first()
        
        db.session.delete(select_registry)
        db.session.commit()
        
        print(f"Delete do registro {select_registry} com sucesso.")
        return jsonify({"message": f"Delete ao registro {select_registry} com sucesso."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": str(e)})
     