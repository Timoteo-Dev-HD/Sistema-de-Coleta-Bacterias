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


@registry_bp.route("/registry", methods=["GET"])
def lista_registry():
    try:
        registros = Registry.query.all()
        
        return jsonify([
            {
                "id": r.id,
                "nome_paciente": r.nome_paciente,
                "data_admissao": r.data_admissao.isoformat(),
                "data_da_coleta": r.data_da_coleta.isoformat(),
                "diagnostico": r.diagnostico,
                "desfecho": r.desfecho
            }
            for r in registros
        ])
        
    except Exception as e:
        return jsonify({"Error": str(e)})   


@registry_bp.route("/registry/<int:id_registry>", methods=["PUT"])
def update_registry(id_registry):
    pass

@registry_bp.route("/registry/<int:id_registry>", methods=["DELETE"])
def delete_registry(id_registry):
    pass