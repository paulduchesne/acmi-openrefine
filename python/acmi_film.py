
# preprocess a table of film data from ACMI API for OpenRefine.

import json
import pandas
import pathlib
import pydash
import tqdm

def replacer(row, flavour, source):

    ''' Function to replace "labels" with Wikidata codes where they already exist against ACMI IDs. '''

    if row[f'{flavour}_id'] in source.keys():
        return source[row[f'{flavour}_id']]
    else:
        return row[f'{flavour}_label']

film_dataframe = pandas.DataFrame(columns=['work_id', 'work_label', 'director_id', 'director_label'])

work_wikidata = dict()
director_wikidata = dict()

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
                    film_dataframe.loc[len(film_dataframe)] = [(api_data['id']), (work_label), (direct['creator_id']), (direct['name'])]
                    if 'creator_wikidata_id' in direct:
                        if direct['creator_wikidata_id']:
                            director_wikidata[(direct['creator_id'])] = direct['creator_wikidata_id']

            wikidata_id = ''
            if 'external_references' in api_data:
                for external_reference in api_data['external_references']:
                    if pydash.get(external_reference, 'source.name') == 'Wikidata':
                        wikidata_id = external_reference['source_identifier']

            if wikidata_id != '':
                work_wikidata[(api_data['id'])] = wikidata_id

film_dataframe['work_label'] = film_dataframe.apply(replacer, flavour='work', source=work_wikidata, axis=1)
film_dataframe['director_label'] = film_dataframe.apply(replacer, flavour='director', source=director_wikidata, axis=1)

dataframe_path = pathlib.Path.cwd() / 'csv' / 'acmi_film.csv'
dataframe_path.parents[0].mkdir(exist_ok=True)

film_dataframe.to_csv(dataframe_path, index=False)

print(len(film_dataframe))
print(film_dataframe.head())
