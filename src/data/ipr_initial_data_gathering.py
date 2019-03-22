"""
This script is intended to pull the entire IPAM database from DDI then
generates and creates a .xls file then saving it to the path directory.
"""
import os
import time
import json
from datetime import datetime
import logging
import requests
import pickle
from dotenv import find_dotenv, load_dotenv
requests.packages.urllib3.disable_warnings()


def write_log(logs, path):
    """
    For use when a view within IPAM does not have a network or network
    container built within the view.
    """
    with open(path, 'w') as file_log:
        for log in logs:
            file_log.write(log + '- Has no network or network container')
            file_log.write('\n')


def wr_output_xls(ddi_data, path, raw_path, logger):
    """
    URLS used to assist in coding with the xlwt module

    URLS:
    https://www.blog.pythonlibrary.org/2014/03/24/
    creating-microsoft-excel-spreadsheets-with-python-and-xlwt

    https://www.bing.com/videos/search?q=adding+lists+to+rows+in+xls+in+
    python&&view=detail&mid=
    DF86F5E6120FCE7BD449DF86F5E6120FCE7BD449&&FORM=VDRVRV 2:41
    """
    import xlwt
    wrk_book = xlwt.Workbook()
    wrk_sheet = wrk_book.add_sheet("DDI", cell_overwrite_ok=True)
    row_number = 0
    row = wrk_sheet.row(row_number)
    for mlist in ddi_data:
        if isinstance(mlist[0], list):
            for ddi_list in mlist:
                for index, col in enumerate(ddi_list):
                    row.write(index, col)
                row_number = row_number + 1
                row = wrk_sheet.row(row_number)
            continue
        if isinstance(mlist[0], str):
            for index, col in enumerate(mlist):
                row.write(index, col)
            row_number = row_number + 1
            row = wrk_sheet.row(row_number)
    try:
        wrk_book.save(path)
        logger.info('Created ddi_workbook.xls')
    except OSError as fileerr:
        filename1 = 'ddi_workbook_' + datetime.now().strftime("%Y%m%d-%H%M%S")\
                    + '.xls'
        path = os.path.join(raw_path, filename1)
        logger.warning('Typically due to a permissions issue!')
        logger.warning('Renaming file to %s, %s', filename1, fileerr)
        wrk_book.save(path)


def process_data(process_json, ea_att_sorted):
    """
    Takes in the raw data from the API calls and splits via ref function
    and appends to a temporary list that then appends to the master list.

    Arguments:
        data_return -- Temp list used for the raw line from the API
    """
    data_return = []
    for i in process_json:
        temp_data_list = [i['_ref'].split('/')[0],
                          i['network'].split('/')[0],
                          '/'+i['network'].split('/')[1],
                          i['network'],
                          i['network_view']]
        if 'comment' not in i:
            temp_data_list.append('')
        else:
            temp_data_list.append(i['comment'])
        if 'extattrs' in i and i['extattrs'] != {}:
            eavalue = i['extattrs']
            for e_att in ea_att_sorted:
                if e_att not in eavalue:
                    temp_data_list.append('')
                    continue
                if isinstance(eavalue[e_att]['value'], list):
                    temp_data_list.append(' '.join(str(e) for e in
                                                   eavalue[e_att]['value']))
                elif e_att in eavalue:
                    temp_data_list.append(eavalue[e_att]['value'])
        else:
            for idx in range(len(ea_att_sorted)):
                temp_data_list.append('')
        if i['utilization']:
            temp_data_list.append(str(i['utilization'])[:-1] + '.' +
                                  str(i['utilization'])[-1])
        else:
            temp_data_list.append('null')
        data_return.append(temp_data_list)
    return data_return


def api_call_network_views(view, logger):
    """
    DDI api call for networks within the 'view' value .  Returns the utf-8
    decoded with a json load.

        Return Variables:
        -- rddijsonnet
    """
    trynetwork = 3
    rnet = None
    for iview in range(trynetwork):
        try:
            rnet = requests.get(PAYLOAD['url'] + "network?_return_fields="
                                                 "extattrs,comment,network,"
                                                 "network_view,utilization&"
                                                 "network_view=" + view,
                                "_max_results=-5000",
                                auth=(PAYLOAD['username'],
                                      PAYLOAD['password']),
                                verify=False)
            break
        except requests.exceptions.ConnectionError as nerrt:
            if iview < trynetwork - 1:
                logger.warning('Network View Retry# %s, %s', view, iview)
                time.sleep(5)
                continue
            else:
                logger.warning('Timeout Error for container view: %s, %s, %s',
                               view, iview, nerrt)
                return []
    return json.loads(rnet.content.decode('utf-8'))


def api_call_networkcontainer_views(view, logger):
    """
    DDI api call for network containers within the 'view' value.  Returns
    the utf-8 decoded with a json load.

        Return Variables:
        -- rddijsonnetcont
    """
    trynetworkview = 3
    rnetcont = None
    for inview in range(trynetworkview):
        try:
            rnetcont = requests.get(PAYLOAD['url'] + "networkcontainer?"
                                                     "_return_fields=extattrs,"
                                                     "comment,utilization,"
                                                     "network,network_view"
                                                     "&network_view=" +
                                    view, "_max_results=-5000",
                                    auth=(PAYLOAD['username'],
                                          PAYLOAD['password']),
                                    verify=False)
            break
        except requests.exceptions.ConnectionError as cerrt:
            if inview < trynetworkview - 1:
                logger.warning('Container View Retry # %s, %s', view, inview)
                time.sleep(5)
                continue
            else:
                logger.warning('Timeout Error for container view: %s, %s, %s',
                               view, inview, cerrt)
                return []
    return json.loads(rnetcont.content.decode('utf-8'))


def get_ddi_ip_data(ddi_ea_att_sorted, title_list, net_views, logger):
    """
    Takes in the following arguments and queries IPAM for each network view.

        Return Variable:
        -- loggedviews - for any network views that have no data
    """
    temp_list = [title_list]
    logged_views = []
    for view in net_views:
        logger.info('Pulling information for View: %s', view)
        rddijsonnet = api_call_network_views(view, logger)
        rddijsonnetcont = api_call_networkcontainer_views(view, logger)
        if isinstance(rddijsonnet, dict) and isinstance(rddijsonnetcont,
                                                        dict):
            continue
        if rddijsonnet and rddijsonnetcont:
            rddijson = rddijsonnet + rddijsonnetcont
            temp_list.append(process_data(rddijson, ddi_ea_att_sorted))
        elif rddijsonnet:
            temp_list.append(process_data(rddijsonnet, ddi_ea_att_sorted))
        elif rddijsonnetcont:
            temp_list.append(process_data(rddijsonnetcont, ddi_ea_att_sorted))
        else:
            logger.info('%s: Has no Network or Network Containers.', view)
            logged_views.append(view)
    return temp_list, logged_views


def get_views():
    """
    Queries DDI for the network views and then extracts the data.

        Return Variable:
        -- views - List of network views
    """
    views = []
    rnetworkview = requests.get(PAYLOAD['url'] + "networkview?",
                                auth=(PAYLOAD['username'],
                                      PAYLOAD['password']),
                                verify=False)
    rutfnetworkview = rnetworkview.content.decode('utf-8')
    rjsonnetworkview = json.loads(rutfnetworkview)
    for raw_view in rjsonnetworkview:
        for key in raw_view.keys():
            if key == 'name':
                views.append(raw_view[key])
    # views = ['UNO']  # Instead of pulling all views.
    return views


def get_ea_attributes():
    """
    Queries DDI for the Extensible Attributes and then extracts the data.
    Also the first attempt at connecting to IPAM.  Built in some error
    checking to report on status of connectivity.

        Return Variable:
        -- eattl - List of extensible attributes
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
    return eattl


def _create_title(title_filename, ea):
    """Creating Workbook Title"""
    title_list = ["DDI Type", "Network", "Subnet", "CIDR", "View", "Comment"]
    title_list.extend(ea)
    title_list.extend(['Utilization in %'])
    with open(title_filename, 'wb') as f_o:
        pickle.dump(title_list, f_o)
    return title_list


def main(project_dir):
    """
    Controller for the raw data pulls needed to acquire the entire IPAM
    DDI IPAM Database.
    """
    # get logger
    logger = logging.getLogger('ipr_initial_data_gathering.py')
    logger.info('Beginning of Script')
    raw_data_path = os.path.join(project_dir, 'data', 'raw')
    ddi_data_path = os.path.join(raw_data_path, 'ddi_workbook.xls')
    title_data_path = os.path.join(raw_data_path, 'ddi_dump_header.pkl')
    logs_data_path = os.path.join(raw_data_path, 'ddi_logs.txt')

    # Query DDI for Extensible Attributes
    logger.info('Pulling EA Attributes: Beginning')
    ddi_ea_attr_sorted = sorted(get_ea_attributes())
    logger.info('Pulling EA Attributes: Completed')

    # Build Title list. Agreed upon IP-Reco Teams format.
    title = _create_title(title_data_path, ddi_ea_attr_sorted)

    # Query DDI for Network Views:
    logger.info('Pulling Network Views: Beginning')
    net_views = get_views()
    logger.info('Pulling Network View: Completed')

    # This step pulls the ddi data, cleans it, then returns the cleaned data.
    logger.info('Pulling DDI Data: Beginning')
    data_list, loggs = get_ddi_ip_data(ddi_ea_attr_sorted,
                                       title,
                                       net_views,
                                       logger)
    logger.info('Pulling DDI Data: Completed')

    # Writes output to an xls file.
    logger.info('Writing Data: Beginning')
    wr_output_xls(data_list, ddi_data_path, raw_data_path, logger)
    logger.info('Writing Data: Completed')

    # Takes any logs received during the get_ddi_ip_data function and writes.
    if loggs:
        write_log(loggs, logs_data_path)
    logger.info('End of Script!')


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

    # PAYLOAD for login to IPAM
    PAYLOAD = {
        'url': os.environ.get("DDI_URL"),
        'username': os.environ.get("DDI_USERNAME"),
        'password': os.environ.get("DDI_PASSWORD")
    }

    # call the main
    main(PROJECT_DIR)
