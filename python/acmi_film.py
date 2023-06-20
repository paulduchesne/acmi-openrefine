
# preprocess a table of film data from ACMI API for OpenRefine.

import json
import pandas
import pathlib
import pydash
import tqdm

film_dataframe = pandas.DataFrame(columns=['work_id', 'work_label', 'director_id', 'director_label'])

api_path = pathlib.Path.cwd() / 'acmi-api' / 'app' / 'json' / 'works'
api_files = [filename for filename in api_path.iterdir() if filename.suffix == '.json']

for api_file in tqdm.tqdm(api_files[:10]):
    with open(api_file, encoding='utf-8') as api_data:
        api_data = json.load(api_data)

    if 'type' in api_data and 'id' in api_data and 'title' in api_data:
        if api_data['type'] == 'Film':
            work_label = api_data['title'].split('=')[0].split('[')[0].split('(')[0]
            if 'creators_primary' in api_data:
                for direct in [x for x in api_data['creators_primary'] if x['role'] == 'director']:
                    film_dataframe.loc[len(film_dataframe)] = [(api_data['id']), (work_label), (direct['creator_id']), (direct['name'])]

dataframe_path = pathlib.Path.cwd() / 'csv' / 'acmi_film.csv'
dataframe_path.parents[0].mkdir(exist_ok=True)

film_dataframe.to_csv(dataframe_path, index=False)
