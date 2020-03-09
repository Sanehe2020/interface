from iface import db

#constants
SMALL_TXT_SIZE = 128
LONG_TXT_SIZE = 256
ANO_SIZE = 4
UF_SIZE = 2

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repr = db.Column(db.String(LONG_TXT_SIZE))
    ano = db.Column(db.String(ANO_SIZE))
    esf_federal = db.Column(db.Boolean)
    esf_estadual = db.Column(db.Boolean) 
    esf_municipal = db.Column(db.Boolean)
    banca = db.Column(db.String(SMALL_TXT_SIZE))
    tipo_mult = db.Column(db.Boolean)
    tipo_ce = db.Column(db.Boolean)
    area = db.Column(db.String(SMALL_TXT_SIZE))
    esc_sup = db.Column(db.Boolean)
    esc_med = db.Column(db.Boolean)
    esc_fund = db.Column(db.Boolean)
    orgao = db.Column(db.String(SMALL_TXT_SIZE)) 
    uf = db.Column(db.String(UF_SIZE))
    municipio = db.Column(db.String(SMALL_TXT_SIZE)) 
    supercargo = db.Column(db.String(SMALL_TXT_SIZE)) 
    cargo = db.Column(db.String(SMALL_TXT_SIZE))
    insc_tot = db.Column(db.Integer) 
    insc_amplo = db.Column(db.Integer) 
    nmax_amplo = db.Column(db.Float)
    corte_amplo = db.Column(db.Float)
    insc_negros = db.Column(db.Integer)
    nmax_negros = db.Column(db.Float)
    corte_negros = db.Column(db.Float)
    insc_def = db.Column(db.Integer)
    nmax_def = db.Column(db.Float)
    corte_def = db.Column(db.Float)
    questoes = db.relationship('Quest', backref='prova', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, ano, supercargo, cargo, esf_federal, esf_estadual, esf_municipal, banca, tipo_mult,
    tipo_ce, area, esc_sup, esc_med, esc_fund, orgao, uf, municipio, insc_tot, insc_amplo, nmax_amplo, corte_amplo,
    insc_negros, nmax_negros, corte_negros, insc_def, nmax_def, corte_def):
        self.ano = ano
        self.esf_federal = True if esf_federal=='true' or esf_federal==True else False
        self.esf_estadual =  True if esf_estadual=='true' or esf_estadual==True else False
        self.esf_municipal = True if esf_municipal=='true' or esf_municipal==True else False
        self.banca = banca
        self.tipo_mult = True if tipo_mult=='true' or tipo_mult==True else False
        self.tipo_ce = True if tipo_ce=='true' or tipo_ce==True else False
        self.area = area
        self.esc_sup = True if esc_sup=='true' or esc_sup==True else False
        self.esc_med = True if esc_med=='true' or esc_med==True else False
        self.esc_fund = True if esc_fund=='true' or esc_fund==True else False
        self.orgao = orgao
        self.uf = uf
        self.municipio = municipio 
        self.supercargo = supercargo
        self.cargo = cargo
        self.insc_tot = insc_tot
        self.insc_amplo = insc_amplo
        self.nmax_amplo = nmax_amplo
        self.corte_amplo = corte_amplo
        self.insc_negros = insc_negros
        self.nmax_negros = nmax_negros
        self.corte_negros = corte_negros
        self.insc_def = insc_def
        self.nmax_def = nmax_def
        self.corte_def = corte_def
        self.repr = self.__repr__()

    def __repr__(self):

        esfs = [self.esf_federal, self.esf_estadual, self.esf_municipal]
        try:
            esf_i = esfs.index(True)
        except:
            esf_i = 4

        if esf_i<3:
            esfera = {
                0: f'Federal',
                1: f'Estadual - {self.uf}',
                2: f'Municipal - {self.municipio}/{self.uf}'
            }[esf_i]
        else:
            esfera = ""

        return f'Prova {self.orgao}({self.banca}/{self.ano}) - {self.cargo} {esfera}'
        


