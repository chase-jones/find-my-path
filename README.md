# Find my Path!

7/5/2020 - Look at the email "Updates From Chase for must up to date info"


#### Overview

The primary purpose of this program is to be able to take in a list of grocery items, and then output an optimal path for shoppers to travel to minimize their time in the store. As features are added, they will be listed below.


#### Needed Files

* Floor Layout of store
* Master SKU list or store item list
* Something to tie the floor layout to the master SKU list. There should be a key in the MasterSKU list which should directly corrolate to lettering on the Floor Layout


#### Structure

1. Main.py will take in one argument for list of groceries either by ID or Item description. Config needs to be done to set up the store, and list of groceries valid for that store
2. Main.py calls Data_Processing.py functions to get a reduced matrix based on items in cart, also taking into consideration of zoning.
3. Program outputs and ordered list which groceries should be shopped in in given order.

##### Data_Processing.py

Path for once a list of grocery lists is given, the task of Data_Processing is:

1. Take the grocery list, and change the item descriptions to item id's
2. Turn item id's to item zones 
3. Produce a reduced matrix for the OR problem to use
4. Turn the ordered list of zones from the OR problem back into an ordered grocery list.

Does not have "inputs" or "Outputs" per se, as this gets imported into main, and main will handle the multiple function capabilities built into data_processing.py. More to come later

##### OR.py

Once reduced matrix and unordered zone list is given, output an ordered list of which zones to go to first, second, and so forth.

Inputs:
* Reduced data matrix [Pandas Dataframe]
* Zone list unordered [Pandas Series]

Outputs
* Zone list ordered [Pandas Series]


##### A_Star_Routing.py

Takes in Pandas Dataframe describing the floor layout, and outputs a distance matrix [large]

Inputs:
* Pandas Dataframe of entire image of floor layout
* Pandas Dataframe describing where all of the different store zones are within the picture. Should tie to format of the DF of the floor layout.

Outputs:
* Pandas Dataframe describing distances between all of the zones.

##### Image_Processing.py

Takes in a .png image, and outputs dataframes that are descriptive of the image

Inputs:
* .png file

Outputs:
* Pandas dataframe that goes pixel by pixel and classifies it into walkable vs. non-walkable space
* Pandas dataframe that tells you where each of the zones are within context of the df above.

##### Main.py

Main file which calls all of the other files

#### Requirements

* Pandas
* Numpy
* [Insert OR related below]




