Welcome to the documentation for the backend of IPR!
====================================================

High level documentation specific to the scripts built for the IPR
project.

Notes to the reader:
--------------------

-   These scripts have been built and run on Python 3.6.6. Recommend
    Python 3.6.6 on up if you are wanting to try these scripts.
-   PyCharm is the IDE used in the running of these scripts within this
    project. These scripts have not been tested from the command line.
-   Refer to .env\_template file to update your .env file for your local
    variables such has URL, Username, Password. You can rename
    .env\_template to .env.
-   Refer to requirements.txt for additional packages you may need to
    install.

Project Organization
--------------------

    +IPR                   <- Root Directory
    -
    --- LICENSE
    --- requirements.txt   <- The requirements file for reproducing the
    ---                         analysis environment.
    --- README.md          <- README
    --- .env               <- .env contains variables used throughout the
    ---                         scripts.  Listed in .gitignore
    --- .env_template      <- a copy of .env with default variables listed.
    ---                         Convert to .env file if needed.
    --- .gitignore         <- files not tracked by Git.
    +-- reports            <- Dir for reports generated for public use.
    +-- data
    +   +-- interim        <- When data is in the middle of being transformed.
    +   +-- processed      <- Final location of finished data transformations.
    +   +-- raw            <- Used for raw data gathered or used in scripts.
    -
    +-- src                <- Source code for use in this project.
    +   +-- __init__.py    <- Makes src a Python module
    +   +
    +   +-- data           <- Scripts to download or generate data
    +   +   +-- ipam_query_full_ipam_data.py
    +   +   +-- ddi_to_master.py
    +   +   +-- master_audit.py
    +   -
    +   +-- features       <- Scripts that perform IPR specific tasks.
    +   +   +-- ipr_report_percent.py
    +   +   +-- ipr_ddi_to_ddi_diff.py
    +   +   +-- ipr_diff_to_ddi_import.py
* * * * *

Request and Compile DDI Data and Generate IPR Requested Output
==============================================================

By following the below listed python scripts you will be following the
step by step process that is currently in use by the IPR Team. To both
request and compile the IB IPAM data into a format as requested by IPR. The
final output being DDI\_to\_IPR.xlsx.

ipam\_query\_app\_full\_report\_xls.py
--------------------------------------

-   Output File: ddi\_workbook.xls

Summary: This is the initial script used to query IB's DDI
solution (AKA DDI).

Script queries DDI for all of the Network Views within DDI. It uses this list
to then query for all of the networks and networkcontainers defined within each
Network View. Once it runs through the list of Network Views it then generates
the output file.

ddi\_to\_master.py
------------------

-   Input File: ddi\_workbook.xls
-   Temp File: DDI\_IPR\_Unsorted.xlsx
-   Output File: DDI\_IPR\_Sorted.xlsx

Summary: This is the script that takes in the ddi data previously
received. It then converts, mashes, separates, and sorts the ddi data and
generates the output file.

master\_audit.py
----------------

-   Interim File: DDI\_IPR\_Sorted.xlsx
-   Output File: DDI-to-IPR.xlsx

Summary:  Script performs a validation check which contains a ip address check
in order to ensure clean network addresses. Once the validation check is passed
it then moves into an index function.  There is a unique index number assigned
to each network.  At which point it performs a conflict check as well as an
overlap check. The index numbers are then used as a tag for when a conflict or
an overlap occurs and then written out to the appropriate cell. This is the
final output for IPR.

Features
========

ipr_report_percent.py
---------------------

-   Input File: DDI\_to\_IPR.xlsx
-   Template File: MASTER \- Report by percent template.xlsx
-   Output File: MASTER \- Report by percent.xlsx

Summary:  Very simple script that takes an input file and a template file.
Add's the data from the Input file to the second sheet of the template file.
Then saves the update .xlsx file as the output file.

ipr_ddi_to_ddi_diff.py
----------------------

-   Input File: Source IPR File
-   Input File: Modified Source IPR File
-   Output File: Potential Updates for DDI.xlsx

Summary:  Script performs a line by line diff between both Input files.  File
names must be updated within the script and downloaded into the appropriate
directory.

ipr_diff_to_ddi_import.py
----------------------

-   Input File: Potential Updates for DDI.xlsx
-   Output File: Merge Import.csv
-   Output File: Override Import.csv
-   Output File: Override to Delete Cells Import.csv

Summary:  For the first run of this script you will want to update the (True
False) ddi_api_call value to True.  This will take the network views from the
input file and query DDI for its data.  Once done, update the ddi_api_call to
false.  Then run the script again.  The script will then perform a diff between
the raw data and the input file.  If there are cells within a row that is
different from what has been listed from the raw data file.  It'll be stored
for the output file based on the matching import criteria.  Please refer to the
manual for csv imports if you have questions on why you would need to do a
merge versus an override.

==================

-   genindex
-   modindex
-   search

