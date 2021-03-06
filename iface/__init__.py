from flask import Flask, render_template, url_for, request, redirect, make_response, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
import datetime, os
from iface.fileutils import *

app = Flask(__name__)

#configs
app.secret_key = 'you will never guess'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '_tmp')
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls'])
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smartlegis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Globals
cache = {}
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Context for the 'flask shell command' and importing of database classes
from iface.db_models.quest import Quest
from iface.db_models.prova import Prova
from iface.db_models.assertiva import Assert
from iface.db_models.oj import Oj
from iface.db_models.sumula import Sumula
from iface.db_models.enunciado import Enunciado
from iface.db_models.lei import Lei, LeiArtigo, LeiArtigoAlinea, LeiInciso, LeiIncisoAlinea, LeiParagrafo, LeiParagrafoAlinea, LeiParagrafoInciso, LeiParagrafoIncisoAlinea
from iface.cacheutils import init_cache, getdbtests, table2cache
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'ma':ma, 'Prova':Prova, 'Quest':Quest, 'Assert':Assert, 'Oj':Oj, 'Sumula':Sumula,
    'Lei':Lei, 'LeiArtigo':LeiArtigo, 'LeiArtigoAlinea':LeiArtigoAlinea, 'LeiInciso':LeiInciso,
    'LeiIncisoAlinea':LeiIncisoAlinea, 'LeiParagrafo':LeiParagrafo, 'LeiParagrafoAlinea':LeiParagrafoAlinea,
    'LeiParagrafoInciso':LeiParagrafoInciso, 'LeiParagrafoIncisoAlinea':LeiParagrafoIncisoAlinea}

@app.route('/')
def index():
    init_cache(cache)
    getdbtests(cache)
    return redirect('mainmenu')

@app.route('/mainmenu')
def mainmenu():
        prova = cache['prova']
        dbtests = cache['dbtests']
        return render_template('mainmenu/mainmenu.html', prova=prova, dbtests=dbtests)

@app.route('/datafromfile', methods=['POST'])
def datafromfile():
    #uploading file
    if 'testfile' not in request.files:
        flash('Sem arquivos na request')
        return redirect('mainmenu')

    arq = request.files['testfile']
    if arq.filename == '':
        flash('Arquivo não selecionado.')
        return redirect('mainmenu')

    if arq and allowed_file(arq.filename):
        filename = secure_filename(arq.filename)
        if filename == '':
            filename=str(datetime.datetime.now().time())+file_ext(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arq.save(filepath)
        flash('Upload de arquivo bem sucedido')

        #parsing file for data
        data = file_parser(filename)(filepath)
        #update cache to show prova from file
        cache.update(data)
        flash("Dados Importados com sucesso!")
        return redirect('mainmenu')
    else:
        flash('Allowed file types are: '+str(app.config['ALLOWED_EXTENSIONS']))
        return redirect('mainmenu')

@app.route('/savetest', methods=['POST'])
def savetest():
    from iface.db_schemas.prova_schema import ProvaSchema
    from iface.db_schemas.quest_schema import QuestSchema

    r = request.form.to_dict()
    ps = ProvaSchema()
    qs = QuestSchema()

    #map prova to db class
    prova = Prova(**r)
    #add prova to database
    db.session.add(prova)
    db.session.commit()

    questoes = []
    quests = cache['prova']['questoes']
    #add quests to database if they exist
    if quests:
        for q in quests:
            #map quest to db class
            quest = Quest(q['numero'],q['materia'],q['texto_associado'],q['corpo'],q['anulada'],q['desatualizada'],q['obs'])
            quest.prova=prova
            db.session.add(quest)
            db.session.commit()
            questoes.append(qs.dump(quest))

    #update cache to correctly display the infos
    p = ps.dump(prova)
    p.update({'questoes':questoes})
    cache.update({'prova':p})

    return cache

@app.route('/cleartest')
def cleartest():
    init_cache(cache)
    return redirect('mainmenu')

@app.route('/questoes', methods=['POST', 'GET'])
def questoes():
    init_cache(cache, 'quest')
    init_cache(cache, 'assert')
    return render_template('questionmenu/questionmenu.html', quests=cache['prova']['questoes'], quest=cache['quest'], cache=cache)

@app.route('/addquestion', methods=['POST'])
def addquestion():
    from iface.db_schemas.quest_schema import QuestSchema
    r = request.form.to_dict()
    quest = Quest(**r)
    quest.prova = Prova.query.filter_by(id=cache['prova']['id']).first()
    #add quest to database
    db.session.add(quest)
    db.session.commit()
    #update cache to show the new question
    qs = QuestSchema()
    qdump = qs.dump(quest) 
    cache['prova']['questoes'].append(qdump)
    return qdump

@app.route('/removequestion', methods=['POST'])
def removequestion():
    question_id = request.form['question_id']
    #remove question from db
    quest = Quest.query.filter_by(id=question_id).first()
    db.session.delete(quest)
    db.session.commit()
    #update cache to remove deleted question
    table2cache(cache, cache['prova']['id'])
    return {'msg': 'question deleted'}

@app.route('/updatequestion', methods=['POST'])
def updatequestion():
    q = request.form
    #temporary model question (probably best using 'schema.load()')
    temp_quest = Quest(q['numero'],q['materia'],q['texto_associado'],q['corpo'],q['anulada'],q['desatualizada'],q['obs'])
    #retrieving db instance
    quest = Quest.query.filter_by(id=q['id']).first()
    #updating question info
    quest.numero = temp_quest.numero
    quest.materia = temp_quest.materia
    quest.texto_associado = temp_quest.texto_associado
    quest.corpo = temp_quest.corpo
    quest.anulada = temp_quest.anulada
    quest.desatualizada = temp_quest.desatualizada
    quest.obs = temp_quest.obs
    db.session.commit()
    #update cache to remove deleted question
    table2cache(cache, cache['prova']['id'])
    return {'msg': 'question updated'}

@app.route('/deltestfromdb', methods=['POST'])
def deltestfromdb():
    #delete test
    test = Prova.query.filter_by(id=request.form['prova_id']).first()
    db.session.delete(test)
    db.session.commit()
    #update cache to reflect changes in the db
    getdbtests(cache)
    return {'msg': 'question deleted'}
    
@app.route('/datafromdb', methods=['POST'])
def datafromdb():
    prova_id = request.form['prova_id']
    table2cache(cache, prova_id)
    return cache

@app.route('/cache')
def cashview():
    return cache

#insert dummy data into the DB
def dummy_data():
    from iface.db_models.quest import Quest
    from iface.db_models.assertiva import Assert

    prova = Prova(2050,'Procurador','Procurador Municipal',False,False, True,'CESPE',False,True,'Jurídica',
        True,False,False,'COGEM','AP','Macapá',1000,990,95,80,200,85,70,50,60,55)
    
    quest1 = Quest(1,'Direito tributário','','Sou o corpitcho de uma questão Neto 1',True,False,
        "una observación")
    quest1.prova = prova

    quest2 = Quest(2,'Direito tributário','','Sou o corpitcho de uma questão Neto 2',False,False,
        "una observación")
    quest2.prova = prova

    assertiva1 = Assert('a','sou a assertiva 1',False,'juris 1','doutrina 1','obs 1')
    assertiva2 = Assert('b','sou a assertiva 2',False,'juris 2','doutrina 2','obs 2')
    assertiva3 = Assert('c','sou a assertiva 3',True,'juris 3','doutrina 3','obs 3')
    assertiva4 = Assert('d','sou a assertiva 4',False,'juris 4','doutrina 4','obs 4')
    assertiva5 = Assert('e','sou a assertiva 5',False,'juris 5','doutrina 5','obs 5')

    assertivas = [assertiva1, assertiva2, assertiva3, assertiva4, assertiva5]
    for assertiva in assertivas:
        assertiva.questao = quest1

    db.session.add(prova)
    db.session.add(quest1)
    db.session.add(quest2)
    db.session.add(assertiva1)
    db.session.add(assertiva2)
    db.session.add(assertiva3)
    db.session.add(assertiva4)
    db.session.add(assertiva5)
    db.session.commit()