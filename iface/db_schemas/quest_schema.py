from iface.db_models.quest import Quest
from iface import ma

class QuestSchema(ma.ModelSchema):
    class Meta:
        model = Quest
        include_fk = True

if __name__ == "__main__":
    q = Quest(1, 'direito const', 'sou um texto associado', 'oahefljfkldsjflksdjfskdfjflnv,mbn,gmngfgjfldkgjfdlkgjfdlgjfdlgjfdlgjkdlkgjfdlkgjfdklgjdfklgjsaul', "false", "true", 'observacion')
    qs = QuestionSchema()
    qs.dump(q)
        


