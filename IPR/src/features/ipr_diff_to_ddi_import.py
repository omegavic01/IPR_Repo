"""Module used in conjunction with ipr_ddi_to_ddi_diff.py.  With the objective
of converting the updates identified into an import sheets for DDI."""
import os
import time
import json
import pickle
import csv
import socket
import struct
import logging
from xlrd import open_workbook
import requests
from dotenv import find_dotenv, load_dotenv


def cidr_to_netmask(cidr):
    """Function that takes a two digit network mask and converts to a subnet
    mask

    Return Value:
        -- netmask
    """
    net_bits = cidr
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask


def _write_output_for_merge_csv(data, file):
    """
    This function writes out a .csv file.
    """
    with open(file, 'w', encoding='utf-8', newline='') as csvfile:
        file_write = csv.writer(csvfile, delimiter='\t')
        for stuff in data:
            if 'network' in stuff:
                for item in stuff[3].keys():
                    if item == 'comment':
                        file_write.writerow(['header-network',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'comment'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[0],
                                             stuff[3]['comment']])
                    if item != 'comment':
                        file_write.writerow(['header-network',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'EA-' + item])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[0],
                                             stuff[3][item]])
            if 'networkcontainer' in stuff:
                for item in stuff[3].keys():
                    if item == 'comment':
                        file_write.writerow(['header-networkcontainer',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'comment'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[0],
                                             stuff[3]['comment']])
                    if item != 'comment':
                        file_write.writerow(['header-networkcontainer',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'EA-' + item])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[0],
                                             stuff[3][item]])


def _write_output_for_overwrite_csv(data, file):
    """
    This function writes out a csv file.
    """
    with open(file, 'w', encoding='utf-8', newline='') as csvfile:
        file_write = csv.writer(csvfile, delimiter='\t')
        for stuff in data:
            if 'network' in stuff:
                for item in stuff[3].keys():
                    if item == 'comment':
                        file_write.writerow(['header-network',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'comment'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[0],
                                             stuff[3]['comment']])
                    if item != 'comment':
                        file_write.writerow(['header-network',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'EA-' + item])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[0],
                                             stuff[3][item]])
            if 'networkcontainer' in stuff:
                for item in stuff[3].keys():
                    if item == 'comment':
                        file_write.writerow(['header-networkcontainer',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'comment'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[0],
                                             stuff[3]['comment']])
                    if item != 'comment':
                        file_write.writerow(['header-networkcontainer',
                                             'address*',
                                             'netmask*',
                                             'network_view',
                                             'EA-' + item])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[0],
                                             stuff[3][item]])


def _write_output_for_delete_csv(data, file):
    """
    This function writes out a csv file.
    """
    with open(file, 'w', encoding='utf-8', newline='') as csvfile:
        file_write = csv.writer(csvfile, delimiter='\t')
        for stuff in data:
            if 'network' in stuff:
                for item in stuff[3].keys():
                    if item == 'comment':
                        file_write.writerow(['header-network',
                                             'address*',
                                             'netmask*',
                                             'comment',
                                             'network_view'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[3]['comment'],
                                             stuff[0]])
                    if item != 'comment':
                        file_write.writerow(['header-network',
                                             'address*',
                                             'netmask*',
                                             'EA-' + item,
                                             'network_view'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[3][item],
                                             stuff[0]])
            if 'networkcontainer' in stuff:
                for item in stuff[3].keys():
                    if item == 'comment':
                        file_write.writerow(['header-networkcontainer',
                                             'address*',
                                             'netmask*',
                                             'comment',
                                             'network_view'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[3]['comment'],
                                             stuff[0]])
                    if item != 'comment':
                        file_write.writerow(['header-networkcontainer',
                                             'address*',
                                             'netmask*',
                                             'EA-' + item,
                                             'network_view'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[3][item],
                                             stuff[0]])


def _get_view_index(views, ddi_data):
    """Takes a compiled list of views and assigns an index in a dictionary as
    indexed by the list of ddi data returned."""
    views_index_temp = {}
    for view in views:
        for enum, ddi_line in enumerate(ddi_data):
            if view == ddi_line[0]['_ref'].split('/')[3]:
                temp_dict = {view: enum}
                views_index_temp.update(temp_dict)
    return views_index_temp


def _get_ea_index(ea_data):
    """Build index table from a sorted list of ea att's.  The index number is
    the value associated to the ea from the update data.  Any changes to EA's
    may require an update here.  Final output is a dict.

    Current Layout as of 3/6/2019:
    ea_data[1]: 6  # Address
    ea_data[2]: 10  # Agency
    ea_data[6]: 4  # City
    ea_data[9]: 3  # Country
    ea_data[10]: 7  # Datacenter
    ea_data[11]: 8  # Division
    ea_data[13]: 13  # Interface Name
    ea_data[17]: 2  # Region_List
    ea_data[20]: 9  # Requester Email
    ea_data[21]: 6  # Site
    ea_data[25]: 11  # Vlan Description
    """
    ea_index_temp = {ea_data[1]: 5, ea_data[2]: 10, ea_data[6]: 4,
                     ea_data[9]: 3, ea_data[10]: 7, ea_data[11]: 8,
                     ea_data[13]: 13, ea_data[17]: 2, ea_data[20]: 9,
                     ea_data[21]: 6, ea_data[25]: 11}
    return ea_index_temp


def _get_rekey_ddi_data(ddi_data, key):
    """Takes a list of lists of dict's and converts to a list of dict's, of
    dicts.  As well as rekey's the dict's with the network address."""
    for enum, item in enumerate(ddi_data):
        ddi_data[enum] = dict(("/".join(d[key].partition(':')[2].
                                        split('/')[0:2]),
                               dict(d, index=index))
                              for (index, d) in enumerate(item))
    return ddi_data


def _get_diff_data(views_index, src_ws, src_n_rows, ea_index, ddi_data):
    """
    This function creates two separate dict's for overlap or merge imports
    based on how DDI handles imports.

    Output List Format:
        -- Ex_List = ['Network_View', 'Network', 'DDI_Type', Dict]
    Return Arguments:
        -- import_merge - data set to go through a merge import process.
        -- import_overwrite - data set to go through an overwrite import
                                process.
    """
    import_merge = []
    import_overwrite = []
    import_delete = []
    for idx in range(src_n_rows):
        if idx == 0:
            continue
        src_row = src_ws.row_values(idx)
        ddi = ddi_data[views_index[src_row[15]]][src_row[1].strip()]

        temp_dict_merge = {}
        temp_dict_overwrite = {}
        temp_dict_delete = {}
        # Comment check.
        if 'comment' not in ddi.keys() and src_row[12].strip() == '':
            pass
        elif 'comment' not in ddi.keys() and src_row[12].strip() != '':
            temp_dict_merge.update({'comment': src_row[12].strip()})
        elif src_row[12].strip() != ddi['comment'] and \
                src_row[12].strip() == '':
            temp_dict_delete.update({'comment': src_row[12].strip()})
        elif src_row[12].strip() != ddi['comment'] and \
                src_row[12].strip() != '':
            temp_dict_overwrite.update({'comment': src_row[12].strip()})
        # EA check
        for key, value in ea_index.items():
            if key not in ddi['extattrs'].keys() and \
                    src_row[value].strip() == '':
                continue
            elif key not in ddi['extattrs'].keys() and \
                    src_row[value].strip() != '':
                temp_dict_merge.update({key: src_row[value]})
            elif src_row[value].strip() != ddi['extattrs'][key]['value'] and \
                    src_row[value].strip() != '':
                temp_dict_overwrite.update({key: src_row[value]})
            elif src_row[value].strip() != ddi['extattrs'][key]['value'] and \
                    src_row[value].strip() == '':
                temp_dict_delete.update({key: src_row[value]})
        if temp_dict_merge:
            import_merge.append([src_row[15].strip(),
                                 src_row[1].strip(),
                                 src_row[14].strip(),
                                 temp_dict_merge])
        if temp_dict_overwrite:
            import_overwrite.append([src_row[15].strip(),
                                     src_row[1].strip(),
                                     src_row[14].strip(),
                                     temp_dict_overwrite])
        if temp_dict_delete:
            import_delete.append([src_row[15].strip(),
                                  src_row[1].strip(),
                                  src_row[14].strip(),
                                  temp_dict_delete])
    return import_merge, import_overwrite, import_delete


def main_phase_one(views, src_ws, ea_path, ddi_path):
    """This function uses four other functions in order to index the data for
    performing diff's.  While the last function call performs the action listed
    below.

    Functions:
        -- _get_view_index
        -- _get_rekey_ddi_data
        -- _get_ea_index
        -- _get_diff_data

    Once the first three functions have completed.  The last function creates
    two separate dict's for overlap or merge imports based on how DDI handles
    imports.

    Return Arguments:
        -- import_merge - data set to go through a merge import process.
        -- import_overwrite - data set to go through an overwrite import
                                process.
    """
    with open(ddi_path, 'rb') as file_in:
        ddi_data = pickle.load(file_in)
    views_index = _get_view_index(views, ddi_data)
    ddi_data = _get_rekey_ddi_data(ddi_data, key="_ref")
    with open(ea_path, 'rb') as file_in:  # API data from DDI EA-Attributes
        ea_index = _get_ea_index(pickle.load(file_in))
    src_n_rows = src_ws.nrows

    return _get_diff_data(views_index, src_ws, src_n_rows, ea_index, ddi_data)


def api_call_network_views(view):
    """DDI api call for networks within the 'view' value .  Returns the utf-8
    decoded with a json load.

        Return Variables:
        -- none
    """
    trynetwork = 3
    rnet = None
    for iview in range(trynetwork):
        try:
            rnet = requests.get(PAYLOAD['url'] + "network?_return_fields="
                                                 "extattrs,comment&"
                                                 "network_view=" + view,
                                "_max_results=-5000",
                                auth=(PAYLOAD['username'],
                                      PAYLOAD['password']),
                                verify=False)
            break
        except requests.exceptions.ConnectionError as nerrt:
            if iview < trynetwork - 1:
                print('Network View retry# ' + view, iview)
                time.sleep(5)
                continue
            else:
                print('Timeout Error for container view: ' + view, ' ',
                      iview, nerrt)
                return []
    return json.loads(rnet.content.decode('utf-8'))


def api_call_networkcontainer_views(view):
    """DDI api call for network containers within the 'view' value.  Returns
    the utf-8 decoded with a json load.

        Return Variables:
        -- none
    """
    trynetworkview = 3
    rnetcont = None
    for inview in range(trynetworkview):
        try:
            rnetcont = requests.get(PAYLOAD['url'] + "networkcontainer?"
                                                     "_return_fields=extattrs,"
                                                     "comment&network_view=" +
                                    view, "_max_results=-5000",
                                    auth=(PAYLOAD['username'],
                                          PAYLOAD['password']),
                                    verify=False)
            break
        except requests.exceptions.ConnectionError as cerrt:
            if inview < trynetworkview - 1:
                print('Container View retry# ' + view, inview)
                time.sleep(5)
                continue
            else:
                print('Timeout Error for container view: ' + view, ' ',
                      inview, cerrt)
                return []
    return json.loads(rnetcont.content.decode('utf-8'))


def get_ea_attributes(path):
    """Queries DDI for the Extensible Attributes and then extracts the data.
    Also the first attempt at connecting to IPAM.  Built in some error
    checking to report on status of connectivity.

        Output Data:
        -- ea_data.pkl
    """
    reattrib = None
    try:
        reattrib = requests.get(PAYLOAD['url'] + "extensibleattributedef?",
                                auth=(PAYLOAD['username'],
                                      PAYLOAD['password']),
                                verify=False)
        reattrib.raise_for_status()
    except requests.exceptions.ConnectionError as eaerrt:
        print("Can't reach IPAM!  Check your VPN or Local access", eaerrt)
        exit()
    except requests.exceptions.HTTPError as eahrrt:
        print('Check your credentials!', eahrrt)
        exit()

    rutfeattrib = reattrib.content.decode('utf-8')
    rjsoneattrib = json.loads(rutfeattrib)
    eattl = []
    for att in rjsoneattrib:
        for key, value in att.items():
            if key == 'name':
                eattl.append(value)
    eattl.sort()
    pickle.dump(eattl, open(path, "wb"))


def get_ddi_ip_data(net_views, ea_path, ddi_path, logger):
    """Takes in the following arguments and queries IPAM by each network view.

        Output:
        ddi_data.pkl
    """
    # Pull down fresh copy of ea-att's
    get_ea_attributes(ea_path)

    # Pull down fresh copy of view data
    ddi_data = []
    for view in net_views:
        print(view)
        ddijsonnet = api_call_network_views(view)
        ddijsonnetcont = api_call_networkcontainer_views(view)
        if isinstance(ddijsonnet, dict) and isinstance(ddijsonnetcont, dict):
            continue
        if ddijsonnet and ddijsonnetcont:
            ddijson = ddijsonnet + ddijsonnetcont
            ddi_data.append(ddijson)
        elif ddijsonnet:
            ddi_data.append(ddijsonnet)
        elif ddijsonnetcont:
            ddi_data.append(ddijsonnetcont)
        else:
            continue
    pickle.dump(ddi_data, open(ddi_path, "wb"))
    logger.info('Change func needddiapicall to False to build import sheets.')
    exit()


def _get_views(n_col, work_sheet):
    """Builds a set list of views from within src_ws"""
    for i in range(n_col):
        if 'View' in work_sheet.row_values(0)[i]:
            view_col = list(set(work_sheet.col_values(i)[1:]))
    return view_col


def main():
    """
    Doc: This script takes the updates made to the master sheet.  Checks and
        converts the data generated from "ipr_ddi_to_ddi_diff.py" into a
        format that can be used for import into DDI.
    Process:
        1. ddi_api_call: is set to False.  If you need to query DDI for new
            network view data you will need to change this to True.  Once the
            data is stored you can change back to False in order avoid the
            query phase of this script.
        2. The data from DDI will be pulled in for comparison with the diff
            data pulled in.  From here this script will convert the data into
            import format for DDI.
        3. Once data is converted the spreadsheet will be created with data
            updated as needed.
    Output Files:
        -- Merge Import.csv
        -- Override Import.csv
        -- Override to Delete Cells Import.csv
    """
    logger = logging.getLogger('ipr_diff_to_ddi_import.py')
    logger.info('Beginning of Script')
    logger.info('Building Paths and File names')

    # Build Directories
    raw_data_path = os.path.join(PROJECT_DIR, 'data', 'raw')
    processed_data_path = os.path.join(PROJECT_DIR, 'data', 'processed')
    reports_data_path = os.path.join(PROJECT_DIR, 'reports')

    # Build File and File path.
    src_file = os.path.join(processed_data_path,
                            'Potential Updates for DDI.xlsx')
    ea_data_file = os.path.join(raw_data_path, 'ea_data.pkl')
    ddi_data_file = os.path.join(raw_data_path, 'ddi_data.pkl')
    merge_file = os.path.join(reports_data_path, 'Merge Import.csv')
    overwrite_file = os.path.join(reports_data_path, 'Override Import.csv')
    delete_file = os.path.join(reports_data_path,
                               'Override to Delete Cells Import.csv')

    logger.info('Loading Data')
    src_wb = open_workbook(src_file)
    src_ws = src_wb.sheet_by_index(0)

    logger.info('Compiling list of views.')
    views = _get_views(src_ws.ncols, src_ws)

    # Update to True if a fresh set of data is needed from ddi.
    ddi_api_call = False
    if ddi_api_call:
        logger.info('ddi_api_call has been set to True.  Querying DDI.')
        get_ddi_ip_data(views, ea_data_file, ddi_data_file, logger)

    # Building data sets for in preparation for writing.
    merge, overwrite, delete = main_phase_one(views,
                                              src_ws,
                                              ea_data_file,
                                              ddi_data_file)

    # Send data off to be written.
    logger.info('Writing Data.  Please refer to the processed dir within data')
    _write_output_for_merge_csv(merge, merge_file)
    _write_output_for_overwrite_csv(overwrite, overwrite_file)
    _write_output_for_delete_csv(delete, delete_file)


if __name__ == '__main__':
    # getting root directory
    PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # setup logger
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    # find .env automatically by walking up directories until it's found
    DOTENV_PATH = find_dotenv()

    # load up the entries as environment variables
    load_dotenv(DOTENV_PATH)

    # Headerrow for IPR Output
    HEADER_ROW = os.environ.get("IPR_HEADER_ROW").split(',')

    # PAYLOAD for login to IPAM
    PAYLOAD = {
        'url': os.environ.get("DDI_URL"),
        'username': os.environ.get("DDI_USERNAME"),
        'password': os.environ.get("DDI_PASSWORD")
    }

    main()
