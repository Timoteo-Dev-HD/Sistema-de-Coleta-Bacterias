from src.settings.extensions import db

class Registry(db.Model):
    
    __tablename__ = "registros"
    
    id = db.Column(db.Integer, primary_key=True)
    nome_paciente = db.Column(db.String(255), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    data_da_coleta = db.Column(db.Date, nullable=False)
    data_encerramento = db.Column(db.Date, nullable=True)
    tempo_coletar = db.Column(db.Integer, nullable=True)
    diagnostico = db.Column(db.String(255), nullable=False)
    desfecho = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"Registry: {self.nome_paciente} - {self.data_admissao}."