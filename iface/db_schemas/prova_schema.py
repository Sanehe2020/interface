from iface.db_models.prova import Prova
from iface import ma

class ProvaSchema(ma.ModelSchema):
    class Meta:
        model = Prova
        include_fk = True


