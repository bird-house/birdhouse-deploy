README
******

This is your user workspace for the JupyterLab environment.

Here is a description of the different directories found in your workspace :

public
======
This directory contains any files that are shared publicly between the users.
This contains, for example, the different WPS outputs files that are not specific to any user.
Note that files shared here are read-only.

tutorial-notebooks
==================
This directory contains different notebooks used to showcase different usages of the birdhouse services and shares
step by step instructions of different use cases.
These notebooks can be executed but cannot be saved as they are read-only.

writable-workspace
==================
This directory contains different subsdirectories that are customized and specialized to the user.
Note that this space is generally writable for the user, so he can create his own files in this directory as desired.

notebooks
---------
This subdirectory is made to contain the different notebooks created by the user.

shapefile_datastore
-------------------
This subdirectory is made to contain different files of the shapefile format for Geoserver. Adding new shapefiles to
this directory will also automatically publish the shapefile to the user's Geoserver workspace.

wps_outputs
-----------
This read-only directory contains the different WPS outputs user files. Note that this directory might not exist if the
user has no user WPS outputs files.
