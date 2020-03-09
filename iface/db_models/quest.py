from iface import db

#constants
SMALL_TXT_SIZE = 128
ANO_SIZE = 4
UF_SIZE = 2

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prova_id = db.Column(db.Integer, db.ForeignKey('prova.id'))
    numero = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(SMALL_TXT_SIZE))
    texto_associado = db.Column(db.Text)
    corpo = db.Column(db.Text)
    anulada = db.Column(db.Boolean)
    desatualizada = db.Column(db.Boolean)
    obs = db.Column(db.Text)
    assertivas = db.relationship('Assert', backref='questao', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, numero, materia, texto_associado, corpo, anulada, desatualizada, obs) :
        self.numero = numero
        self.materia = materia
        self.texto_associado = texto_associado
        self.corpo = corpo
        self.anulada = True if anulada=='true' or anulada==True else False
        self.desatualizada = True if desatualizada=='true' or desatualizada==True else False
        self.obs = obs

    def __repr__(self):
        return f'Quest(id:{self.id}, nro:{self.numero}, {self.corpo[:30]})'


