from flask import (
    Blueprint,
    request,
    jsonify
)

export_bp = Blueprint("export", __name__, url_prefix="/export")

@export_bp.route("/", meehotds=["GET"])
def exporta_relatorio_mes():
    pass