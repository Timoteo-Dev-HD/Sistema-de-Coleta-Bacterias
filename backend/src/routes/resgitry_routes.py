from flask import (
    Blueprint,
    request,
    jsonify
)

from src.models.registry_model import Registry
from src.settings.extensions import db

registry_bp = Blueprint("registry", __name__)

@registry_bp.route("/registry", methods=["POST"])
def create_registry():
    pass

from sqlalchemy import asc

@registry_bp.route("/registry", methods=["GET"])
def lista_registry():
    try:
        registros = (
            Registry.query
            .order_by(asc(Registry.nome_paciente))
            .all()
        )

        return jsonify([
            {
                "id": r.id,
                "nome_paciente": r.nome_paciente,
                "data_admissao": r.data_admissao.isoformat() if r.data_admissao else None,
                "data_da_coleta": r.data_da_coleta.isoformat() if r.data_da_coleta else None,
                "diagnostico": r.diagnostico,
                "desfecho": r.desfecho
            }
            for r in registros
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@registry_bp.route("/registry/<int:id_registry>", methods=["PUT"])
def update_registry(id_registry):
    pass

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
     