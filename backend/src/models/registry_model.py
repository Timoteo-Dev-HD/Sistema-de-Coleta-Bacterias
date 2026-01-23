from src.settings.extensions import db

class Registry(db.Model):

    __tablename__ = "registros"

    id = db.Column(db.Integer, primary_key=True)
    nome_paciente = db.Column(db.String(255), nullable=False)
    data_admissao = db.Column(db.Date, nullable=True)
    data_da_coleta = db.Column(db.Date, nullable=True)
    data_encerramento = db.Column(db.Date, nullable=True)
    tempo_coletar = db.Column(db.Integer, nullable=True)
    diagnostico = db.Column(db.String(255), nullable=True)
    desfecho = db.Column(db.String(255), nullable=True)

    # Novos dados clínicos
    notificacao = db.Column(db.String(4), nullable=True)
    dialise = db.Column(db.String(4), nullable=True)
    material_coletada = db.Column(db.String(255), nullable=True)
    microorganismo = db.Column(db.String(255), nullable=True)
    local = db.Column(db.String(50), nullable=True)

    # Antibióticos já existentes
    amicacina = db.Column(db.String(50), nullable=True)
    ampicilina = db.Column(db.String(50), nullable=True)
    amoxicilina = db.Column(db.String(50), nullable=True)
    amoxicilina_clavulanato = db.Column(db.String(50), nullable=True)
    amp_sulbactam = db.Column(db.String(50), nullable=True)
    azitromicina = db.Column(db.String(50), nullable=True)
    cefalexina = db.Column(db.String(50), nullable=True)
    cefazolina = db.Column(db.String(50), nullable=True)
    cefepime = db.Column(db.String(50), nullable=True)

    # Restante dos antimicrobianos
    ceftazidime = db.Column(db.String(50), nullable=True)
    cefoxitina = db.Column(db.String(50), nullable=True)
    ceftriaxone = db.Column(db.String(50), nullable=True)
    cefuroxime = db.Column(db.String(50), nullable=True)
    ciprofloxacino = db.Column(db.String(50), nullable=True)
    clindamicina = db.Column(db.String(50), nullable=True)
    daptomicina = db.Column(db.String(50), nullable=True)
    eritromicina = db.Column(db.String(50), nullable=True)
    ertapenem = db.Column(db.String(50), nullable=True)
    gentamicina = db.Column(db.String(50), nullable=True)
    imipenem = db.Column(db.String(50), nullable=True)
    levofloxacino = db.Column(db.String(50), nullable=True)
    linezolida = db.Column(db.String(50), nullable=True)
    moxifloxacina = db.Column(db.String(50), nullable=True)
    oxacilina = db.Column(db.String(50), nullable=True)
    ofloxacina = db.Column(db.String(50), nullable=True)
    penicilina = db.Column(db.String(50), nullable=True)
    meropenem = db.Column(db.String(50), nullable=True)
    minociclina = db.Column(db.String(50), nullable=True)
    norfloxacina = db.Column(db.String(50), nullable=True)
    piperacilina_tazobactam = db.Column(db.String(50), nullable=True)
    polimixina_b = db.Column(db.String(50), nullable=True)
    rifampicina = db.Column(db.String(50), nullable=True)
    streptomicina = db.Column(db.String(50), nullable=True)
    trimetoprim_sulfametoxazol = db.Column(db.String(50), nullable=True)
    teicoplanina = db.Column(db.String(50), nullable=True)
    tetraciclina = db.Column(db.String(50), nullable=True)
    tigeciclina = db.Column(db.String(50), nullable=True)
    vancomicina = db.Column(db.String(50), nullable=True)

    # Antifúngicos e outros
    anfotericina_b = db.Column(db.String(50), nullable=True)
    fluconazol = db.Column(db.String(50), nullable=True)
    ketoconazol = db.Column(db.String(50), nullable=True)
    voriconazol = db.Column(db.String(50), nullable=True)
    nitrofurantoina = db.Column(db.String(50), nullable=True)
    aztreonam = db.Column(db.String(50), nullable=True)
    cloranfenicol = db.Column(db.String(50), nullable=True)
    colistina = db.Column(db.String(50), nullable=True)

    # Betalactâmicos especiais
    ceftazidima_avibactam = db.Column(db.String(50), nullable=True)
    ceftolozano_tazobactam = db.Column(db.String(50), nullable=True)
    ceftarolina = db.Column(db.String(50), nullable=True)
    cefotaxime = db.Column(db.String(50), nullable=True)
    ceftibufen = db.Column(db.String(50), nullable=True)

    # Campo livre
    observacao = db.Column(db.String(255), nullable=True)

    # Data de criação do registro
    data_criacao = db.Column(db.Date, nullable=True)
    data_atualizacao = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Registry: {self.nome_paciente} - {self.data_admissao}"
