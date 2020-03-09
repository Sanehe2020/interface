from iface import db

#constants
SMALL_TXT_SIZE = 128
LONG_TXT_SIZE = 256
ANO_SIZE = 4
UF_SIZE = 2

class Lei(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    esfera = db.Column(db.String(SMALL_TXT_SIZE))
    uf = db.Column(db.String(UF_SIZE))
    municipio = db.Column(db.String(SMALL_TXT_SIZE)) 
    tipo = db.Column(db.String(SMALL_TXT_SIZE)) 
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    livro = db.Column(db.String(SMALL_TXT_SIZE))
    titulo = db.Column(db.String(SMALL_TXT_SIZE))
    capitulo = db.Column(db.String(SMALL_TXT_SIZE))
    secao = db.Column(db.String(SMALL_TXT_SIZE))
    subsecao = db.Column(db.String(SMALL_TXT_SIZE))
    alterada = db.Column(db.Boolean)
    artigos = db.relationship('LeiArtigo', backref='lei', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, esfera, uf, municipio, tipo, diploma, ano, livro, titulo, 
    capitulo, secao, subsecao, alterada):
        self.esfera = esfera
        self.uf = uf
        self.municipio = municipio
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano
        self.livro = livro
        self.titulo = titulo
        self.capitulo = capitulo
        self.secao = secao
        self.subsecao = subsecao
        self.alterada = True if alterada=='true' or alterada==True else False

    def __repr__(self):
        estado = {
            'federal':f'',
            'estadual':f'- {self.uf}',
            'municipal': f'- {self.municipio},{self.uf}'
        }[self.esfera.lower()]
        return f'Lei n.{self.diploma}/{self.ano}{estado}'

class LeiArtigo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_id = db.Column(db.Integer, db.ForeignKey('lei.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    alineas = db.relationship('LeiArtigoAlinea', backref='artigo', cascade='all, delete-orphan', lazy='dynamic')
    incisos = db.relationship('LeiInciso', backref='artigo', cascade='all, delete-orphan', lazy='dynamic')
    paragrafos = db.relationship('LeiParagrafo', backref='artigo', cascade='all, delete-orphan', lazy='dynamic')
    

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

######################  Lei --> Artigo --> Alínea ####################
class LeiArtigoAlinea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_artigo_id = db.Column(db.Integer, db.ForeignKey('lei_artigo.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

######################  Lei --> Artigo --> Inciso --> Alínea ####################
class LeiInciso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_artigo_id = db.Column(db.Integer, db.ForeignKey('lei_artigo.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    alineas = db.relationship('LeiIncisoAlinea', backref='inciso', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

class LeiIncisoAlinea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_inciso_id = db.Column(db.Integer, db.ForeignKey('lei_inciso.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

######################  Lei --> Artigo --> Parágrafo --> Alínea ####################
class LeiParagrafo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_artigo_id = db.Column(db.Integer, db.ForeignKey('lei_artigo.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    alineas = db.relationship('LeiParagrafoAlinea', backref='paragrafo', cascade='all, delete-orphan', lazy='dynamic')
    incisos = db.relationship('LeiParagrafoInciso', backref='paragrafo', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

class LeiParagrafoAlinea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_paragrafo_id = db.Column(db.Integer, db.ForeignKey('lei_paragrafo.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

######################  Lei --> Artigo --> Parágrafo --> Inciso --> Alínea ####################
class LeiParagrafoInciso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_paragrafo_id = db.Column(db.Integer, db.ForeignKey('lei_paragrafo.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    alineas = db.relationship('LeiParagrafoIncisoAlinea', backref='inciso', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'

class LeiParagrafoIncisoAlinea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lei_paragrafo_inciso_id = db.Column(db.Integer, db.ForeignKey('lei_paragrafo_inciso.id'))
    dispositivo = db.Column(db.String(SMALL_TXT_SIZE))
    tipo = db.Column(db.String(SMALL_TXT_SIZE))
    diploma = db.Column(db.Integer)
    ano = db.Column(db.Integer)

    def __init__(self, dispositivo, tipo, diploma, ano):
        self.dispositivo = dispositivo
        self.tipo = tipo
        self.diploma = diploma
        self.ano = ano

    def __repr__(self):
        return f'{self.dispositivo} - redação dada  por {self.tipo} n.{self.diploma}/{self.ano}'