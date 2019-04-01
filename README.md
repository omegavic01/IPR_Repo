Welcome to the documentation for the backend of IPR!
====================================================

High level documentation specific to the scripts built for the IPR
project.

Notes to the reader:
--------------------

-   These scripts have been built and run on Python 3.6.6. Recommend
    Python 3.6.6 on up if you are wanting to try these scripts.
-   PyCharm Community Edition 2017.2.4 is the IDE used in the running of these
    scripts within this project. These scripts have not been tested from the
    command line.
-   Refer to .env\_template file to update your .env file for your local
    variables such has URL, Username, Password. You can rename
    .env\_template to .env.  The .env file lives in the same directory as
    .env\_template.
-   Refer to requirements.txt for the list of python modules used for these
    scripts.

Project Organization
--------------------

    +IPR                   <- Root Directory
    ---
    --- LICENSE
    --- requirements.txt   <- The python packages used for reproducing the
    ---                         analysis environment.
    --- README.md          <- README (What is displayed on the GitHub Repo.)
    --- .env               <- .env contains variables used throughout the
    ---                         scripts.  Listed in .gitignore.  Not downloaded
    ---                         from GitHub.  Will need to create and update
    ---                         from .env_template.
    --- .env_template      <- a copy of .env with default variables listed.
    ---                         Convert to .env file if needed.
    --- .gitignore         <- files not tracked by Git.
    +-- reports            <- Dir for reports generated for IPR use.
    +-- data
    +-- +-- interim        <- When data is in the middle of being transformed.
    +-- +-- processed      <- Final location of finished data transformations.
    +-- +-- raw            <- Used for raw data gathered or used in scripts.
    ---
    +-- src                <- Source code for use in this project.
    +-- --- __init__.py
    +-- ---
    +-- +-- data           <- Scripts to download or generate data
    +-- +-- --- ipr_main_script.py
    +-- +-- --- ipr_initial_data_gathering.py
    +-- +-- --- ipr_format_ddi.py
    +-- +-- --- ipr_audit_ddi.py
    --- ---
    +-- +-- features       <- Scripts that perform IPR specific tasks.
    +-- +-- --- ipr_report_percent.py
    +-- +-- --- ipr_clean_vrf_check.py
    +-- +-- --- ipr_ddi_to_ddi_diff.py
    +-- +-- --- ipr_diff_to_ddi_import.py
* * * * *

Request and Compile DDI Data and Generate IPR Requested Output
==============================================================

By following the below listed python scripts you will be following the
step by step process that is currently in use by the IPR Team. To both
request and compile the IB IPAM data into a format as required by IPR. The
final output being DDI\_to\_IPR.xlsx.

ipr\_main\_script.py
--------------------------------------

Summary: This script houses the five scripts used to create the IPR formatted
data from the IP database.  The request was to have one script that runs the
scripts needed to create the data thereby removing the manual process.

ipr\_initial\_data\_gathering.py
--------------------------------------

-   Output File: ddi\_workbook.xls

Summary: This is the initial script used to query IB's DDI
solution.

Script queries DDI for all of the Network Views within DDI. It uses this list
to then query all of the networks and networkcontainers defined within each
Network View. Once it runs through the list of Network Views it then generates
the output file.

ipr\_format\_ddi.py
------------------

-   Input File: ddi\_workbook.xls
-   Temp File: DDI\_IPR\_Unsorted.xlsx
-   Output File: DDI\_IPR\_Sorted.xlsx

Special Note: If new EA's are renamed.  This is the script to update!

Summary: This is the script that takes in the ddi data previously
received. It then converts, mashes, separates, and sorts the ddi data and
generates the output file.

ipr\audit\_ddi.py
----------------

-   Interim File: DDI\_IPR\_Sorted.xlsx
-   Output File: DDI-to-IPR.xlsx

Summary:  Script begins with an ip address validation check in order to ensure
clean network addresses within the data. Once the validation check is passed it
 then moves into an index function.  There is a unique index number assigned to
 each network.  At which point it performs a conflict check as well as an
 overlap check. The index numbers are then used as a tag for when a conflict or
 an overlap occurs and then written out to the appropriate cell. This is the
 final output for IPR.

Features
========

ipr_report_percent.py
---------------------

-   Input File: DDI\_to\_IPR.xlsx
-   Template File: MASTER \- Report by percent template.xlsx (IPR has template)
-   Output File: MASTER \- Report by percent.xlsx

Summary:  Very simple script that takes an input file and a template file.
Add's the data from the Input file to the second sheet of the template file.
Then saves the update .xlsx file as the output file.

ipr_clean_vrf_check.py
---------------------

-   Input Data: ddi\_to\_ipr.pkl
-   Updates Fil: DDI\_to\_IPR.xlsx

Summary:  Creates two new tabs in the DDI\_to\_IPR.xlsx spreadsheet.  One tab
contains any vrf's identified that do not have any conflicts with any other
vrf's.  The second tab created lists the vrf 3 digit identifier and any
conflicting vrf's that it may have.

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

+   Potential Output File based on results.
-   Output File: Merge Import.csv
-   Output File: Override Import.csv
-   Output File: Override to Delete Cells Import.csv
-   Output File: Add Import.csv
-   Output File: Delete Import.csv
-   Output File: Merge Dup Import.csv
-   Output File: Merge Leaf Import.csv
-   Output File: Merge Ignore Import.csv

Additional Features: If the following has been added in the disposition field
of the IPR sheet.[add, del, ignore, dup, leaf] This script will run a separate
function and create separate import sheets for each.

Summary:  For the first run of this script you will want to update ddi_api_call
 value to True.  This will take the network views from the input file and query
 DDI for its data.  Once done, update the ddi_api_call to false.  Then run the
script again.  The script will then perform a diff between the raw data and
the input file.  If there are cells within a row that is different from what
has been listed from the raw data file.  It'll be stored for the output file
based on the matching import criteria.  Please refer to the manual for csv
imports if you have questions on why you would need to do a merge versus an
override.
