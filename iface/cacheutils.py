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
    from sqlalchemy import asc

    dbtests = {'dbtests':[]}
    provas = prova.Prova.query.order_by(asc('ano')).all()
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

    pschema = prova_schema.ProvaSchema()
    qschema = quest_schema.QuestSchema()
    aschema = assert_schema.AssertSchema()

    #dumping test and questions
    temp = pschema.dump(p)
    temp.update({'questoes':qschema.dump(quests, many=True)})

    #expanding assertivas for each question
    for q in temp['questoes']:
        assertivas = assertiva.Assert.query.filter_by(questao_id=q['id']).all()
        q['assertivas'] = aschema.dump(assertivas, many=True)

    #finally updating cache
    cache.update({'prova':temp})