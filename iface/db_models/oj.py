from iface import db

#constants
SMALL_TXT_SIZE = 128
LONG_TXT_SIZE = 256
ANO_SIZE = 4
UF_SIZE = 2
LETRA_SIZE = 1

class Oj(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entidade = db.Column(db.String(SMALL_TXT_SIZE))
    numero = db.Column(db.Integer)
    cancelada = db.Column(db.Boolean)

    def __init__(self, entidade, numero, cancelada):
        self.entidade = entidade
        self.numero = numero
        self.cancelada = True if cancelada=='true' or cancelada==True else False

    def __repr__(self):
        status = {True:"<cancelada>", False:""}[self.cancelada]
        return f'OJ n.{self.numero} - {self.entidade}{status}'
        


