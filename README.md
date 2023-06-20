# ACMI OpenRefine

Preprocessing scripts and resources for using ACMI API data with Wikidata via OpenRefine.

## Run Preprocessor

The `./run.sh` script will ensure that API data is pulled and current, and generate CSVs for use in OpenRefine.

## Install OpenRefine

Installation options for OpenRefine can be found [here](https://openrefine.org/download). Version 3.7 has been used in all testing so far.

On Linux the downloaded tar.gz file can be unpackaged and then launched by running `./refine` from within the unpacked directory. This will result in a service running at http://127.0.0.1:3333/.

## Reconciling Data

To begin working with OpenRefine, select one of the CSVs as data source. For this example we are using `acmi_film.csv`. Select `Next`.

Rename the project as desired (under `Project name`) and then select `Create project`.

Select arrow next to `work_label` and then `Reconcile` -> `Start reconciling...`

The only service which will likely be visible will be `Wikidata reconci.link (en)`. Select this.

The reconciliation service should automaticatly detect that each cell should be against the type of `film (Q11424)`, otherwise you may need to specify this under `Reconcile against type`.

Add `director_label` by selecting that checkbox on the right hand side, and `As property` enter `P57`.

Select `Start reconciling...`

This should result in a table where entries are highlighted in dark blue if they have been succesfully matched with Wikidata items. It is possible to hover over these to confirm that the description matches what is expected. Entities which have been matched in the past will automatically be picked up.

Other entires will need disambiguation as OpenRefine cannot determine a match on its own. Here you may select the proper candidate from the list by using the checkbox icon on the left of each option. 

It is quite possible that some entires do not exist in Wikidata and will need to be created. If this is the case, select `Create new item` at the bottom of the options.

