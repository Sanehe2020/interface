from iface.db_models.assertiva import Assert
from iface import ma

class AssertSchema(ma.ModelSchema):
    class Meta:
        model = Assert
        include_fk = True


