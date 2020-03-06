from iface.db_models import prova, quest
from iface.db_schemas import prova_schema, quest_schema

def init_cache(cache, mode='all'):
    p = prova.Prova('','','',False, False,False,'',False,False,'',False,False,False,'','','',0,0,0.0,0.0,0,0.0,0.0,0,0.0,0.0)
    q = quest.Quest(0, '','','',False,False,'')
    ps = prova_schema.ProvaSchema()
    qs = quest_schema.QuestSchema()

    #blank test with no questions
    blank_test = {'prova':ps.dump(p)}
    blank_test['prova']['questoes'] = []

    #blank quest template with no assertivas
    blank_quest = {'quest':qs.dump(q)}
    blank_quest['quest']['assertivas'] = []

    #blank assertiva template - missing assertiva implementation
    blank_assert = {
        'assert':
        {
            'letra':  '',
            'corpo': '',
            'correta': False,
            'jurispridencia': '',
            'doutrinha': '',
            'obs': ''
        }
    }

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
    data = {
        'prova':
        {
            'ano': 2050,
            'supercargo': 'Procurador',
            'esf_federal': False,
            'esf_estadual': False, 
            'esf_municipal': True, 
            'banca': 'CESPE',
            'tipo_mult': False, 
            'tipo_ce': True,
            'area': 'Jurídica', 
            'esc_sup': True, 
            'esc_med': False, 
            'esc_fund': False, 
            'orgao': 'COGEM', 
            'uf': 'AP', 
            'municipio': 'Macapá', 
            'supercargo': 'Procurador', 
            'cargo': 'Procurador Municipal',
            'insc_tot': 1000, 
            'insc_amplo': 990, 
            'nmax_amplo': 95, 
            'corte_amplo': 80, 
            'insc_negros': 200, 
            'nmax_negros': 85, 
            'corte_negros': 70,
            'insc_def': 50, 
            'nmax_def': 60,
            'corte_def': 55,
            'questoes': []
        }
    }

    dummy_quest1 = {
        'id': 1,
        'numero': 1,
        'materia': 'Direito tributário',
        'texto_associado': None,
        'corpo': 'Sou o corpitcho de uma questão Neto 1',
        'anulada': True,
        'desatualizada': False,
        'obs': "una observación",
        'assertivas': []
    }

    dummy_quest2 = {
        'id': 2,
        'numero': 2,
        'materia': 'Direito tributário',
        'texto_associado': None,
        'corpo': 'Sou o corpitcho de uma questão Neto 2',
        'anulada': True,
        'desatualizada': False,
        'obs': "una observación",
        'assertivas': []
    }
    
    dummy_assertiva1 = {
        'letra':  'a',
        'corpo': 'sou a assertiva 1',
        'correta': False,
        'jurispridencia': 'juris 1',
        'doutrinha': 'doutrina 1',
        'obs': 'obs1'
    }
    dummy_assertiva2 = {
        'letra':  'b',
        'corpo': 'sou a assertiva 2',
        'correta': False,
        'jurispridencia': None,
        'doutrinha': None,
        'obs': None

    }
    dummy_assertiva3 = {
        'letra':  'c',
        'corpo': 'sou a assertiva 3',
        'correta': True,
        'jurispridencia': None,
        'doutrinha': None,
        'obs': None
    }
    dummy_assertiva4 = {
        'letra':  'd',
        'corpo': 'sou a assertiva 4',
        'correta': False,
        'jurispridencia': None,
        'doutrinha': None,
        'obs': None
    }

    dummy_quest1['assertivas'] = [dummy_assertiva1, dummy_assertiva2, dummy_assertiva3, dummy_assertiva4]
    data['prova']['questoes'] = [dummy_quest1, dummy_quest2]
    cache.update(data)