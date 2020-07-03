# Find my Path!

## Overview

The primary purpose of this program is to be able to take in a list of grocery items, and then output an optimal path for shoppers to travel to minimize their time in the store. As features are added, they will be listed below.


## Needed Files

* Floor Layout of store
* Master SKU list or store item list
* Something to tie the floor layout to the master SKU list. There should be a key in the MasterSKU list which should directly corrolate to lettering on the Floor Layout


## Structure

1. Main.py will take in one argument for list of groceries either by ID or Item description. Config needs to be done to set up the store, and list of groceries valid for that store
2. Main.py calls Data_Processing.py functions to get a reduced matrix based on items in cart, also taking into consideration of zoning.
3. Program outputs and ordered list which groceries should be shopped in in given order.



