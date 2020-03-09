from iface import db

#constants
SMALL_TXT_SIZE = 128
LONG_TXT_SIZE = 256
ANO_SIZE = 4
UF_SIZE = 2
LETRA_SIZE = 1

#relação entre Assertivas e OJs
ojs = db.Table('ojs',
    db.Column('assert_id', db.Integer, db.ForeignKey('assert.id'), primary_key=True),
    db.Column('oj_id', db.Integer, db.ForeignKey('oj.id'), primary_key=True)
)

#relação entre Assertivas e Sumulas
sumulas = db.Table('sumulas',
    db.Column('assert_id', db.Integer, db.ForeignKey('assert.id'), primary_key=True),
    db.Column('sumula_id', db.Integer, db.ForeignKey('sumula.id'), primary_key=True)
)

#relação entre Assertivas e Enunciados
enunciados = db.Table('enunciados',
    db.Column('assert_id', db.Integer, db.ForeignKey('assert.id'), primary_key=True),
    db.Column('enunciado_id', db.Integer, db.ForeignKey('enunciado.id'), primary_key=True)
)

#relação entre Assertivas e Leis
leis = db.Table('leis',
    db.Column('assert_id', db.Integer, db.ForeignKey('assert.id'), primary_key=True),
    db.Column('lei_id', db.Integer, db.ForeignKey('lei.id'), primary_key=True)
)

class Assert(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('quest.id'))
    letra = db.Column(db.String(LETRA_SIZE))
    corpo = db.Column(db.Text)
    correta = db.Column(db.Boolean)
    jurisprudencia = db.Column(db.Text)
    doutrina = db.Column(db.Text)
    obs = db.Column(db.Text)
    ojs = db.relationship('Oj', secondary=ojs, lazy='subquery', 
                        backref=db.backref('assertivas', lazy=True))
    sumulas = db.relationship('Sumula', secondary=sumulas, lazy='subquery',
                        backref=db.backref('assertivas', lazy=True))
    enunciados = db.relationship('Enunciado', secondary=enunciados, lazy='subquery',
                        backref=db.backref('assertivas', lazy=True))
    leis = db.relationship('Lei', secondary=leis, lazy='subquery',
                        backref=db.backref('assertivas', lazy=True))

    def __init__(self, letra, corpo, correta, jurisprudencia, doutrina, obs):
        self.letra = letra
        self.corpo = corpo
        self.correta = True if correta=='true' or correta==True else False
        self.jurisprudencia = jurisprudencia
        self.doutrina = doutrina
        self.obs = obs

    def __repr__(self):
        return f'{self.letra}) {self.corpo[:30]}'
        


