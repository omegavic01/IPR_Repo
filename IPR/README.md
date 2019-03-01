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
    +
    +-- LICENSE
    +-- requirements.txt   <- The requirements file for reproducing the analysis environment, e.g. pip freeze
    +-- README.md          <- Shortcut for the high level documentation in html format.  To be used as the guide for this project.
    +-- .env               <- .env contains variables used throughout the scripts.  Listed in .gitignore
    +-- .env_template      <- a copy of .env with default variables listed.  Convert to .env file if needed.
    +-- .gitignore         <- files not tracked by Git.
    +-- data
    +   +-- external       <- (Unused)
    +   +-- interim        <- When data is in the middle of being transformed.
    +   +-- processed      <- Final location of finished products
    +   +-- raw            <- Used for raw data gathered or used in scripts
    +
    +-- docs               <- Path to index.html.
    +
    +-- src                <- Source code for use in this project.
    +   +-- __init__.py    <- Makes src a Python module
    +   +
    +   +-- data           <- Scripts to download or generate data
    +   +   +-- ipam_query_full_ipam_data.py
    +   +   +-- ddi_to_master.py
    +   +   +-- master_audit.py
    +   +-- features       <- Scripts that generate reports
    +   +   +-- ipr_report_percent.py
* * * * *

Request and Compile DDI Data and Generate IPR Requested Output
==============================================================

By following the below listed python scripts you will be following the
step by step process that is currently in use by the IPR Team. To both
request and compile the IB DDI IPAM data into a format as
requested by IPR. The final output being DDI\_to\_IPR.xlsx. Future
development of scripts and documentation for creating import sheets for
IB based off of changes to DDI\_to\_IPR.xlsx has been road mapped.

ipam\_query\_app\_full\_report\_xls.py
--------------------------------------

-   Output File: ddi\_workbook.xls

Summary: This is the initial script used to query IB's DDI
solution (AKA DDI).

From here this queries DDI for all of the Network Views within DDI. It
uses this list to then query for all of the networks and
networkcontainers defined within each Network View. Once it runs through
the list of Network Views it then generates the output file listed
above.

ddi\_to\_master.py
------------------

-   Input File: ddi\_workbook.xls
-   Output File: DDI\_IPR\_Unsorted.xlsx

Summary: This is the script that takes in the ddi data previously
received. It then converts, mashes, and separates the ddi data and
generates the output file listed above.

master\_audit.py
----------------

-   Input File: DDI\_IPR\_Unsorted.xlsx
-   Interim File: DDI\_IPR\_Sorted.xlsx
-   Output File: DDI-to-IPR.xlsx

Summary: This script will sort all of the Networks listed within the
input file. From here it will perform a validation check which contains
a list of filters based on IPR's needs. Once the validation check is
passed it then moves into an index function. There is a unique index
number assigned to each network listed within the input file. At which
point it performs a conflict check as well as an overlap check. The
index numbers are then used as a tag for when a conflict or an overlap
occurs and updated in the appropriate cell. This is the final output for
IPR.

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


Indices and tables
==================

-   genindex
-   modindex
-   search

