# ACMI OpenRefine

Resources for using ACMI API data with Wikidata via OpenRefine.

## Installing OpenRefine

Installation options for OpenRefine can be found [here](https://openrefine.org/download). Version 3.7 has been used for all testing so far.

On Linux the downloaded tar.gz file can be unpackaged and then launched from the command line by running `./refine` from within the unpacked directory. Mac and Windows should launch from the application icon. This will result in a service running at http://127.0.0.1:3333/.

## Using OpenRefine

To begin working with OpenRefine, select a csv as data source. For this example, we are using `acmi_film.csv`. Select `Next`.

![](png/01.png)

Rename the project as desired (under `Project name`) and then select `Create project`.

![](png/02.png)

Select the down arrow next to `work_label` and then `Reconcile` -> `Start reconciling...`

![](png/03.png)

The only service which will likely be visible will be `Wikidata reconci.link (en)`. Select it.

![](png/04.png)

The reconciliation service should automatically detect that each cell from the `work_label` column is of type `film (Q11424)`, otherwise you may need to specify this manually under `Reconcile against type`.

![](png/05.png)

Add `director_label` by selecting that checkbox on the right-hand side, and `As property` enter `P57`. By providing the director information, you are increasing the chance of making a correct connection. 

![](png/06.png)

Select `Start reconciling...`

![](png/07.png)

This should result in a table where entries are highlighted in dark blue if they have been successfully automatically matched with Wikidata items. Be aware that these matches can be made dependent on title scarcity, as much as by using supplementary information. It is possible to hover over these to confirm that the description matches what is expected. 

![](png/08.png)

Other entries will require disambiguation, as OpenRefine cannot determine a match on its own. You may select the proper candidate from the list by using the checkbox icon on the left of each option. 

![](png/09.png)

It is quite possible that some entries do not exist in Wikidata and will need to be created. If this is the case, select the checkbox next to `Create new item`.

![](png/10.png)

As we are now going to upload, you are required to login using Wikidata account credentials. These can be provided under `Manage Wikibase account...`

![](png/11.png)

A schema can now be applied to determine how the linked tabular source can be transformed into data statements. Select `Manage schemas`.

![](png/12.png)

Load the `acmi_film.json` schema supplied in this repository.

![](png/13.png)

To apply the schema, select `Edit Wikibase schema`.

![](png/14.png)

Select the schema from the dropdown.

![](png/15.png)

This schema will automatically map your columns into appropriate Wikidata data statements.

![](png/16.png)

`Preview` will display the statements as they will look once written across to Wikidata.

![](png/17.png)

Upload the statements via `Upload Edits to Wikibase...`

![](png/18.png)

The `upload edits` window will display any warnings. It is also possible to add a summary describing information about the upload batch. Select `Upload edits`.

![](png/19.png)

Edits should be visible immediately in Wikidata.

![](png/20.png)

Consulting the version history of the entity should also confirm the source of the edits.

![](png/21.png)

## License

The contents of this repo are provided under the MIT license.
