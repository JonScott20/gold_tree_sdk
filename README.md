# Gold Tree SDK

This package is used to connect with the Gold Tree Solar Farm API. The Gold Tree Solar Farm is located near Cal Poly, San Luis Obispo, CA. 

# Installation
`$ pip install goldtree`

# Configuration
In order to authenticate with the API, you will need to provide valid credentials. These credentials will need to be set in the settings.py file of the installed package. In order to determine where the package is installed, run the following commands:
~~~~
$ python
>>> import goldtree
>>> goldtree
<module 'goldtree' from '/Users/jon/anaconda3/lib/python3.7/site-packages/goldtree/__init__.py'>
>>> exit()
$ cd /Users/jon/anaconda3/lib/python3.7/site-packages/goldtree
vim settings.py
~~~~

Replace
~~~~
USERNAME = ""
PASSWORD = ""
~~~~

with 

~~~~
USERNAME = "MyUsername"
PASSWORD = "MyPassword"
~~~~

and save the file.

## Verification
~~~~
$ python
>>> import goldtree
>>> gt = goldtree.RequestManager()
>>> gt.authentication_status
Success
~~~~

# Usage
Observe that the start and end variables are Unix timestamps.
~~~~
>>> import goldtree
>>> gt = goldtree.RequestManager()
>>> start = 1542874200
>>> end = 1555939500
>>> power_df = gt.get_power_production_data(start, end, "tenminute")
~~~~
