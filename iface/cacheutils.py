from iface.db_models import prova, quest, assertiva
from iface.db_schemas import prova_schema, quest_schema, assert_schema

def init_cache(cache, mode='all'):
    #instantiating 'blank' models and its schemas
    p = prova.Prova('','','',False, False,False,'',False,False,'',False,False,False,'','','',
        0,0,0.0,0.0,0,0.0,0.0,0,0.0,0.0)
    q = quest.Quest(0, '','','',False,False,'')
    a = assertiva.Assert('','',False,'','','')
    pschema = prova_schema.ProvaSchema()
    qschema = quest_schema.QuestSchema()
    aschema = assert_schema.AssertSchema()

    #blank test with no questions
    blank_test = {'prova':pschema.dump(p)}
    blank_test['prova']['questoes'] = []

    #blank quest template with no assertivas
    blank_quest = {'quest':qschema.dump(q)}
    blank_quest['quest']['assertivas'] = []

    #blank assertiva template with no legis
    blank_assert = {'assert':aschema.dump(a)}
    blank_assert['assert']['ojs'] = []
    blank_assert['assert']['sumulas'] = []
    blank_assert['assert']['enunciados'] = []
    blank_assert['assert']['leis'] = []

    mode_selector = {
        'prova':   lambda c: c.update(blank_test),
        'quest':   lambda c: c.update(blank_quest),
        'assert':  lambda c: c.update(blank_assert)
    }

    valid_keys = [key for key in mode_selector.keys()] + ['all']
    if mode not in valid_keys:
        return f'invalid mode. Allowed modes are: {valid_keys}'

    if mode in mode_selector.keys():
        mode_selector[mode](cache)

    if mode == 'all':
        for m in mode_selector.keys():
            mode_selector[m](cache)

    #no tests in the database
    dbtests = {'dbtests':[]}
    cache.update(dbtests)

    return True

def getdbtests(cache):
    from sqlalchemy import desc

    dbtests = {'dbtests':[]}
    provas = prova.Prova.query.order_by(desc('ano')).all()
    for p in provas:
        dbtests['dbtests'].append({
           'id': p.id,
           'repr': p.__repr__() 
        })

    cache.update(dbtests)
    return True
    
def table2cache(cache, prova_id):
    p = prova.Prova.query.filter_by(id=prova_id).first()
    quests = quest.Quest.query.filter_by(prova_id=prova_id).all()

    ps = prova_schema.ProvaSchema()
    qs = quest_schema.QuestSchema()

    temp = ps.dump(p)
    temp.update({'questoes':qs.dump(quests, many=True)})
    cache.update({'prova':temp})

def dummy_data(cache):
    dummy_prova = prova.Prova(2050,'Procurador','Procurador Municipal',False,False, True,'CESPE',False,True,'Jurídica',
        True,False,False,'COGEM','AP','Macapá',1000,990,95,80,200,85,70,50,60,55)
    dummy_quest1 = quest.Quest(1,'Direito tributário','','Sou o corpitcho de uma questão Neto 1',True,False,
        "una observación")
    dummy_quest2 = quest.Quest(2,'Direito tributário','','Sou o corpitcho de uma questão Neto 2',False,False,
        "una observación")
    dummy_assertiva1 = assertiva.Assert('a','sou a assertiva 1',False,'juris 1','doutrina 1','obs 1')
    dummy_assertiva2 = assertiva.Assert('b','sou a assertiva 2',False,'juris 2','doutrina 2','obs 2')
    dummy_assertiva3 = assertiva.Assert('c','sou a assertiva 3',True,'juris 3','doutrina 3','obs 3')
    dummy_assertiva4 = assertiva.Assert('d','sou a assertiva 4',False,'juris 4','doutrina 4','obs 4')
    dummy_assertiva5 = assertiva.Assert('e','sou a assertiva 5',False,'juris 5','doutrina 5','obs 5')

    pschema = prova_schema.ProvaSchema()
    qschema = quest_schema.QuestSchema()
    aschema = assert_schema.AssertSchema()

    questoes = [dummy_quest1, dummy_quest2]
    qdumps = [qschema.dump(questao) for questao in questoes]
    assertivas = [dummy_assertiva1, dummy_assertiva2, dummy_assertiva3, dummy_assertiva4, dummy_assertiva5]
    adumps = [aschema.dump(assertiva) for assertiva in assertivas]

    for qdump in qdumps:
        qdump['assertivas'] = adumps

    test = pschema.dump(dummy_prova)
    test['questoes'] = qdumps

    cache.update({'prova':test})