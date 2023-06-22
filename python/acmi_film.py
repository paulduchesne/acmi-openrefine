
# preprocess a table of film data from the ACMI API for use in OpenRefine.

import json
import pandas
import pathlib
import pydash
import requests
import tqdm

def replacer(row, flavour, source):

    ''' Function to replace "labels" with Wikidata codes where they already exist against ACMI IDs. '''

    if row[f'{flavour}_id'] in source.keys():
        return source[row[f'{flavour}_id']]
    else:
        return row[f'{flavour}_label']

def value_extract(row, column):

    ''' Extract dictionary values. '''
    
    return pydash.get(row[column], 'value')

def sparql_query(query, service):

    ''' Send sparql request, and formulate results into a dataframe. '''
    
    response = requests.get(service, params={'format': 'json', 'query': query}, timeout=120)
    results = pydash.get(response.json(), 'results.bindings')
    data_frame = pandas.DataFrame.from_dict(results)
    for column in data_frame.columns:
        data_frame[column] = data_frame.apply(value_extract, column=column, axis=1)

    return data_frame

# pull a list of existing links on Wikidata side.

query = '''select ?acmi_id where { ?wikidata_id wdt:P7003 ?acmi_id }'''
wikidata_acmi_links = sparql_query(query, 'https://query.wikidata.org/sparql')    

film_dataframe = pandas.DataFrame(columns=['work_id', 'work_label', 'director_id', 'director_label'])
work_wikidata, director_wikidata = dict(), dict()

api_path = pathlib.Path.cwd() / 'acmi-api' / 'app' / 'json' / 'works'
api_files = [filename for filename in api_path.iterdir() if filename.suffix == '.json']

for api_file in tqdm.tqdm(api_files):
    with open(api_file, encoding='utf-8') as api_data:
        api_data = json.load(api_data)

    if 'type' in api_data and 'id' in api_data and 'title' in api_data:
        if api_data['type'] == 'Film':
            work_label = api_data['title'].split('=')[0].split('[')[0].split('(')[0]
            if 'creators_primary' in api_data:
                for direct in [x for x in api_data['creators_primary'] if x['role'] == 'director']:
                    film_dataframe.loc[len(film_dataframe)] = [(f"works/{api_data['id']}"), (work_label), (f"creators/{direct['creator_id']}"), (direct['name'])]
                    if 'creator_wikidata_id' in direct:
                        if direct['creator_wikidata_id']:
                            director_wikidata[f"creators/{direct['creator_id']}"] = direct['creator_wikidata_id']

            wikidata_id = ''
            if 'external_references' in api_data:
                for external_reference in api_data['external_references']:
                    if pydash.get(external_reference, 'source.name') == 'Wikidata':
                        wikidata_id = external_reference['source_identifier']

            if wikidata_id != '':
                work_wikidata[f"works/{api_data['id']}"] = wikidata_id

# these function calls would apply wikidata ids to replace labels where known.

film_dataframe['work_label'] = film_dataframe.apply(replacer, flavour='work', source=work_wikidata, axis=1)
film_dataframe['director_label'] = film_dataframe.apply(replacer, flavour='director', source=director_wikidata, axis=1)

# remove works where a wikidata link already exists.

film_dataframe = film_dataframe.loc[~film_dataframe.work_id.isin(wikidata_acmi_links.acmi_id.unique())]

# note that we are not substituting in creator links which only exist wikidata-side

# render a sample of ten items for import into OpenRefine.

dataframe_path = pathlib.Path.cwd() / 'csv' / 'acmi_film.csv'
dataframe_path.parents[0].mkdir(exist_ok=True)
film_dataframe.sample(10).to_csv(dataframe_path, index=False)
