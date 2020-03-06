import csv

def allowed_file(filename):
    return '.' in filename and file_ext(filename) in ['csv', 'xls']

def file_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def file_parser(filename):
    selector = {
        'csv': parse_csv,
        'xls': parse_xls
    }
    return selector[file_ext(filename)]
    
def parse_xls(xls_file):
    pass

def parse_csv(csv_file):
    with open(csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        entry = csv_reader.__next__()

        #adjusting multiple choice fields
        entry['esf_federal']=False if entry['esfera']!='esf_federal' else True
        entry['esf_estadual']=False if entry['esfera']!='esf_estadual' else True
        entry['esf_municipal']=False if entry['esfera']!='esf_municipal' else True

        entry['tipo_mult']=False if entry['tipo']!='tipo_mult' else True
        entry['tipo_ce']=False if entry['tipo']!='tipo_ce' else True

        entry['esc_sup']=False if entry['nivel']!='esc_sup' else True
        entry['esc_med']=False if entry['nivel']!='esc_med' else True
        entry['esc_fund']=False if entry['nivel']!='esc_fund' else True

        entry['questoes'] = []
        q1 = {
                'numero': 1,
                'materia': 'direito civil',
                'texto_associado': 'blah blah blah',
                'corpo': 'el couerpo',
                'anulada': False,
                'desatualizada': True,
                'obs':'la observacion'
        }

        q2 = {
                'numero': 2,
                'materia': 'direito civil2',
                'texto_associado': 'blah blah blah2',
                'corpo': 'el couerpo2',
                'anulada': False,
                'desatualizada': True,
                'obs':'la observacion2'
        }

        q3 = {
                'numero': 3,
                'materia': 'direito civil3',
                'texto_associado': 'blah blah blah3',
                'corpo': 'el couerpo3',
                'anulada': False,
                'desatualizada': True,
                'obs':'la observacion3'
        }

        entry['questoes'] = [q1, q2, q3]

        return {'prova': entry}
  
