from flask import (
    Blueprint,
    request,
    jsonify
)
from datetime import datetime
from sqlalchemy import asc
from src.models.registry_model import Registry
from src.settings.extensions import db
from src.utils.util import ANTIBIOTICOS

registry_bp = Blueprint("registry", __name__)

@registry_bp.route("/registry", methods=["POST"])
def create_registry():
    return "hello world!";


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
                
                # Datas de registros
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
    data = request.json or {}

    registry = Registry.query.get_or_404(id_registry)

    # =========================
    # 🔹 Helpers
    # =========================
    def parse_date(value):
        """
        Converte 'YYYY-MM-DD' → date
        Converte '', None → None
        """
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None

    def empty_to_none(value):
        return value if value not in ("", None) else None

    # =========================
    # 🔹 Datas
    # =========================
    registry.data_admissao = parse_date(data.get("data_admissao"))
    registry.data_da_coleta = parse_date(data.get("data_da_coleta"))
    registry.data_encerramento = parse_date(data.get("data_encerramento"))

    # =========================
    # 🔹 Campos clínicos
    # =========================
    registry.tempo_coletar = empty_to_none(data.get("tempo_coletar"))
    registry.diagnostico = empty_to_none(data.get("diagnostico"))
    registry.desfecho = empty_to_none(data.get("desfecho"))
    registry.notificacao = empty_to_none(data.get("notificacao"))
    registry.dialise = empty_to_none(data.get("dialise"))
    registry.local = empty_to_none(data.get("local"))
    registry.observacao = empty_to_none(data.get("observacao"))

    # =========================
    # 🔹 Dados do exame
    # =========================
    registry.material_coletada = empty_to_none(data.get("material_coletada"))
    registry.microorganismo = empty_to_none(data.get("microorganismo"))

    for ab in ANTIBIOTICOS:
        if ab in data:
            setattr(registry, ab, empty_to_none(data.get(ab)))

    # =========================
    # 🔹 Commit
    # =========================
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registro atualizado com sucesso"
    }), 200


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
     