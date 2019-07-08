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


def _write_output_for_add_csv(data, file):
    """
    This function writes out a .csv file for an import type: add.
    """
    ea_index = _get_ea_index()
    with open(file, 'w', encoding='utf-8', newline='') as csvfile:
        file_write = csv.writer(csvfile, delimiter='\t')
        for stuff in data:
            if 'networkcontainer' in stuff:
                # Initial Row fields built
                if stuff[16] == 'DDI':
                    stuff[16] = ''
                temp_data = [stuff[14],
                             stuff[1].split('/')[0],
                             stuff[1].split('/')[1],
                             stuff[15]]
                temp_header = ['header-networkcontainer',
                               'address*',
                               'netmask*',
                               'network_view']
                # Check for comments
                if stuff[12]:
                    if '\n' in stuff[12]:
                        temp_data.append(stuff[12].replace('\n', ',').strip(','))
                        temp_header.append('comment')
                    else:
                        temp_data.append(stuff[12])
                        temp_header.append('comment')
                # Check for EA's
                for key in ea_index.keys():
                    if key in ['Datacenter', 'IPR Designation'] and \
                            ',' in stuff[ea_index[key]]:
                        items = stuff[ea_index[key]].split(',')
                        for item in items:
                            temp_header.append('EA-'+key)
                            temp_header.append('EAInherited-'+key)
                            temp_data.append(item.strip())
                            temp_data.append('OVERRIDE')
                        continue
                    if stuff[ea_index[key]]:
                        temp_header.append('EA-'+key)
                        temp_header.append('EAInherited-'+key)
                        temp_data.append(stuff[ea_index[key]].strip())
                        temp_data.append('OVERRIDE')
                # Write Header Row on new line.
                file_write.writerow(temp_header)
                # Write data Row on new line.
                file_write.writerow(temp_data)
            if 'network' in stuff:
                # Initial Row fields built
                if stuff[16] == 'DDI':
                    stuff[16] = ''
                temp_data = [stuff[14],
                             stuff[1].split('/')[0],
                             cidr_to_netmask(stuff[1].
                                             split('/')[1]),
                             stuff[15]]
                temp_header = ['header-network',
                               'address*',
                               'netmask*',
                               'network_view']
                # Check for comments
                if stuff[12]:
                    if '\n' in stuff[12]:
                        temp_data.append(stuff[12].replace('\n', ',').strip(','))
                        temp_header.append('comment')
                    else:
                        temp_data.append(stuff[12])
                        temp_header.append('comment')
                # Check for EA's
                for key in ea_index.keys():
                    if key in ['Datacenter', 'IPR Designation'] and \
                                    ',' in stuff[ea_index[key]]:
                        items = stuff[ea_index[key]].split(',')
                        for item in items:
                            temp_header.append('EA-'+key)
                            temp_header.append('EAInherited-'+key)
                            temp_data.append(item.strip())
                            temp_data.append('OVERRIDE')
                        continue
                    if stuff[ea_index[key]]:
                        temp_header.append('EA-'+key)
                        temp_header.append('EAInherited-'+key)
                        temp_data.append(stuff[ea_index[key]])
                        temp_data.append('OVERRIDE')
                # Write Header Row on new line.
                file_write.writerow(temp_header)
                # Write data Row on new line.
                file_write.writerow(temp_data)


def _write_output_for_merge_csv(data, file):
    """
    This function writes out a .csv file for an import type: merge.
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
                                             'EA-' + item,
                                             'EAInherited-' + item])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[0],
                                             stuff[3][item],
                                             'OVERRIDE'])
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
                                             'EA-' + item,
                                             'EAInherited-' + item])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[0],
                                             stuff[3][item],
                                             'OVERRIDE'])


def _write_output_for_merge_disposition_csv(data, file):
    """
    This function writes out a .csv file for an import type: merge.
    """
    with open(file, 'w', encoding='utf-8', newline='') as csvfile:
        file_write = csv.writer(csvfile, delimiter='\t')
        for stuff in data:
            if 'network' in stuff:
                file_write.writerow(['header-network',
                                     'address*',
                                     'netmask*',
                                     'network_view',
                                     'EA-IPR Designation',
                                     'EAInherited-IPR Designation'])
                file_write.writerow([stuff[2],
                                     stuff[1].split('/')[0],
                                     cidr_to_netmask(stuff[1].
                                                     split('/')[1]),
                                     stuff[0],
                                     stuff[3],
                                     'OVERRIDE'])
            if 'networkcontainer' in stuff:
                file_write.writerow(['header-networkcontainer',
                                     'address*',
                                     'netmask*',
                                     'network_view',
                                     'EA-IPR Designation',
                                     'EAInherited-IPR Designation'])
                file_write.writerow([stuff[2],
                                     stuff[1].split('/')[0],
                                     stuff[1].split('/')[1],
                                     stuff[0],
                                     stuff[3],
                                     'OVERRIDE'])


def _write_output_for_delete_csv(data, file):
    """
    This function writes out a .csv file for an import type: delete.
    """
    with open(file, 'w', encoding='utf-8', newline='') as csvfile:
        file_write = csv.writer(csvfile, delimiter='\t')
        for stuff in data:
            if 'network' in stuff:
                file_write.writerow(['header-network',
                                     'address*',
                                     'netmask*',
                                     'network_view'])
                file_write.writerow([stuff[2],
                                     stuff[1].split('/')[0],
                                     cidr_to_netmask(stuff[1].
                                                     split('/')[1]),
                                     stuff[0]])
            if 'networkcontainer' in stuff:
                file_write.writerow(['header-networkcontainer',
                                     'address*',
                                     'netmask*',
                                     'network_view'])
                file_write.writerow([stuff[2],
                                     stuff[1].split('/')[0],
                                     stuff[1].split('/')[1],
                                     stuff[0]])


def _write_output_for_override_csv(data, file):
    """
    This function writes out a csv file for an import type: override.
    """
    ea_index = _get_ea_index()
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
                        if item in ['Datacenter', 'IPR Designation'] and \
                                        ',' in stuff[3][item]:
                            temp_data = [stuff[2],
                                         stuff[1].split('/')[0],
                                         cidr_to_netmask(stuff[1].
                                                         split('/')[1]),
                                         stuff[0]]
                            temp_header = ['header-network',
                                           'address*',
                                           'netmask*',
                                           'network_view']
                            items = stuff[3][item].split(',')
                            for it in items:
                                temp_header.append('EA-' + item)
                                temp_header.append('EAInherited-' + item)
                                temp_data.append(it.strip())
                                temp_data.append('OVERRIDE')
                            # Write Header Row on new line.
                            file_write.writerow(temp_header)
                            # Write data Row on new line.
                            file_write.writerow(temp_data)
                        else:
                            file_write.writerow(['header-network',
                                                 'address*',
                                                 'netmask*',
                                                 'network_view',
                                                 'EA-' + item,
                                                 'EAInherited-' + item])
                            file_write.writerow([stuff[2],
                                                 stuff[1].split('/')[0],
                                                 cidr_to_netmask(stuff[1].
                                                                 split('/')[1]),
                                                 stuff[0],
                                                 stuff[3][item],
                                                 'OVERRIDE'])
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
                        if item in ['Datacenter', 'IPR Designation'] and \
                                        ',' in stuff[3][item]:
                            temp_data = [stuff[2],
                                         stuff[1].split('/')[0],
                                         stuff[1].split('/')[1],
                                         stuff[0]]
                            temp_header = ['header-networkcontainer',
                                           'address*',
                                           'netmask*',
                                           'network_view']
                            items = stuff[3][item].split(',')
                            for it in items:
                                temp_header.append('EA-' + item)
                                temp_header.append('EAInherited-' + item)
                                temp_data.append(it.strip())
                                temp_data.append('OVERRIDE')
                            # Write Header Row on new line.
                            file_write.writerow(temp_header)
                            # Write data Row on new line.
                            file_write.writerow(temp_data)
                        else:
                            file_write.writerow(['header-networkcontainer',
                                                 'address*',
                                                 'netmask*',
                                                 'network_view',
                                                 'EA-' + item,
                                                 'EAInherited-' + item])
                            file_write.writerow([stuff[2],
                                                 stuff[1].split('/')[0],
                                                 stuff[1].split('/')[1],
                                                 stuff[0],
                                                 stuff[3][item],
                                                 'OVERRIDE'])


def _write_output_for_override_blanks_csv(data, file):
    """
    This function writes out a csv file for an import type: override.
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
                                             'EAInherited-' + item,
                                             'network_view'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             cidr_to_netmask(stuff[1].
                                                             split('/')[1]),
                                             stuff[3][item],
                                             'OVERRIDE',
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
                                             'EAInherited-' + item,
                                             'network_view'])
                        file_write.writerow([stuff[2],
                                             stuff[1].split('/')[0],
                                             stuff[1].split('/')[1],
                                             stuff[3][item],
                                             'OVERRIDE',
                                             stuff[0]])


def _get_view_index(views, ddi_data):
    """Takes a compiled list of views and assigns an index in a dictionary as
    indexed by the list of ddi data returned."""
    views_index_temp = {}
    for view in views:
        for enum, ddi_line in enumerate(ddi_data):
            if view == ddi_line[0]['network_view']:
                temp_dict = {view: enum}
                views_index_temp.update(temp_dict)
    return views_index_temp


def _get_ea_index():
    """
    Manually build index table for the ea att's.  The index number is
    the value associated to the ea from the update data.  If an EA has been
    renamed in IB.  An update will be required here. If an EA has had its name
    added to Master an update will be required here. Final output is a dict.
    """
    ea_index_temp = {'Address': 5, 'Agency': 10, 'City': 4, 'Country': 3,
                     'Datacenter': 7, 'Division': 8, 'Interface Name': 13,
                     'Region_List': 2, 'Requester Email': 9, 'Site': 6,
                     'VLAN Description': 11, 'IPR Designation': 16}
    return ea_index_temp


def _get_rekey_ddi_data(ddi_data):
    """Takes a list of lists of dict's and converts to a list of dict's, of
    dicts.  As well as rekey's the dict's with the network address."""
    for enum, item in enumerate(ddi_data):
        ddi_data[enum] = dict((d['network'],
                               dict(d, index=index))
                              for (index, d) in enumerate(item))
    return ddi_data


def _get_diff_data(views_index, src_data, ea_index, ddi_data):
    """
    This function creates two separate dict's for overlap or merge imports
    based on how DDI handles imports.

    Output List Format:
        -- Ex_List = ['Network_View', 'Network', 'DDI_Type', Dict]
    Return Arguments:
        -- import_merge - data set to go through a merge import process.
        -- import_delete - data set to go through a delete import process.
        -- import_override - data set to go through an override import
        -- import_override_to_blank - data set to go through an override import
    """

    def _add_and_del():
        """Handles the add's and del import's."""
        for add_or_del_row in src_data:
            # Add Check.
            if 'add' in add_or_del_row[0]:
                if add_or_del_row[1] in \
                        ddi_data[views_index[add_or_del_row[15]]]:
                    errored_list.append(add_or_del_row)
                    continue
                else:
                    import_add.append(add_or_del_row)
                    continue

            # delete check
            if 'del' in add_or_del_row[0] and add_or_del_row[1] in \
                    ddi_data[views_index[add_or_del_row[15]]][
                        add_or_del_row[1]]:
                import_delete.append([add_or_del_row[15],
                                      add_or_del_row[1],
                                      add_or_del_row[14]])
                continue
            unused_list.append(add_or_del_row)

    def _ea_in_disposition_col0_and_empty_ipr_d_col():
        """Disposition col0 check and an empty ipr disposition column."""
        for disposition_row in unused_list:
            # Check disposition
            ddi_index = views_index[disposition_row[15]]
            # Checks disposition column value and checks for IPR D value.
            # If no IPR D in extattrs dict stores the src data for updates.
            if disposition_row[0] in ea_ipr_d_values and 'IPR Designation' not\
                    in ddi_data[ddi_index][disposition_row[1]]['extattrs']:
                import_merge_disposition.append(
                    [disposition_row[15],
                     disposition_row[1],
                     disposition_row[14],
                     disposition_row[0]])

    def _comment_check():
        """Function for checking ipam comment attribute."""
        for comment_row in unused_list:
            ddi_index = views_index[comment_row[15]]
            # Checks for empty src value and empty ddi data value.
            # Continues if True.
            if 'comment' not in ddi_data[ddi_index][comment_row[1]]\
                    and comment_row[12] == '':
                continue
            # Checks a non-empty src value and updates if an
            # empty ddi data value.
            if 'comment' not in ddi_data[ddi_index][comment_row[1]] and \
                    comment_row[12] != '':
                import_merge.append([comment_row[15],
                                     comment_row[1],
                                     comment_row[14],
                                     {'comment': comment_row[12]}])
                continue
            # Checks diff against src value and a populated value in the
            # ddi data and replaces with src value.
            if comment_row[12] != \
                    ddi_data[ddi_index][comment_row[1]]['comment']:
                import_override.append([comment_row[15],
                                        comment_row[1],
                                        comment_row[14],
                                        {'comment': comment_row[12]}])
                continue

    def _non_listed_ea_columns_check():
        """Checks non-listable ea columns."""
        for ea_row in unused_list:
            # dup Check in disposition
            ddi_index = views_index[ea_row[15]]
            for key, value in ea_index.items():
                # ea attributes that could be listed.
                if key == 'Datacenter' or key == 'IPR Designation':
                    continue
                # Checks for empty src value and empty ddi data value.
                # Continues if True.
                if key not in ddi_data[ddi_index][ea_row[1]]['extattrs'] and \
                        ea_row[value] in ['', 'DDI']:
                    continue
                # Checks a non-empty src value and updates if an
                # empty ddi data value.
                if key not in ddi_data[ddi_index][ea_row[1]]['extattrs'] \
                        and ea_row[value] not in ['', 'DDI']:
                    import_merge.append([ea_row[15],
                                         ea_row[1],
                                         ea_row[14],
                                         {key: ea_row[value]}])
                    continue
                # Checks diff against src value and a populated value in the
                # ddi data and replaces with src value.
                if ea_row[value] != \
                        ddi_data[ddi_index][
                            ea_row[1]]['extattrs'][key]['value']:
                    import_override.append([ea_row[15],
                                            ea_row[1],
                                            ea_row[14],
                                            {key: ea_row[value]}])
                    continue

    def _listed_ea_column_check():
        """Checks non-listable ea columns."""
        for ea_row in unused_list:
            ddi_index = views_index[ea_row[15]]
            # This check is performed in
            # _ea_in_disposition_col0_and_empty_ipr_d_col
            if ea_row[0] in ea_ipr_d_values and \
                    'IPR Designation' not in \
                    ddi_data[ddi_index][ea_row[1]]['extattrs']:
                continue
            # Update IPR D src column with ea_row[0] for processing.
            # WORK IN PROGRESS
            elif ea_row[0] in ea_ipr_d_values and 'IPR Designation' \
                    in ddi_data[ddi_index][ea_row[1]]['extattrs']:
                pass
            # Processing listable columns.
            for key, value in ea_index.items():
                # Skip's unused keys.
                if key not in ['Datacenter', 'IPR Designation']:
                    continue
                # Check for blank column and blank source column.
                if key not in ddi_data[ddi_index][ea_row[1]]['extattrs'] and \
                        ea_row[value] in ['', 'DDI']:
                    continue
                # Check for Disposition col, check for comma not in IPR D col
                # value, check value in IPR D col to ea ipr d attribute list,
                # check IPR D col value eq ddi value.
                # On not listed IPR D values.
                if key == 'IPR Designation':
                    if ea_row[0] in ea_ipr_d_values \
                        and ',' not in ea_row[16] \
                            and ea_row[16] in ea_ipr_d_values:
                        ea_row[16] = ea_row[16] + ',' + ea_row[0]
                        import_override.append([ea_row[15].strip(),
                                                ea_row[1].strip(),
                                                ea_row[14].strip(),
                                                {key: ea_row[16]}])
                        continue
                # Check for Disposition col, check for comma not in IPR D col
                # value, check value in IPR D col to ea ipr d attribute list,
                # check IPR D col value eq ddi value.
                # On not listed IPR D values.
                    elif ea_row[0] in ea_ipr_d_values \
                            and ',' not in ea_row[16] \
                            and ea_row[16] not in ea_ipr_d_values:
                        import_override.append([ea_row[15].strip(),
                                                ea_row[1].strip(),
                                                ea_row[14].strip(),
                                                {key: ea_row[0]}])
                        continue
#                # Check Disposition col. and if IPR D listed value needs
#                # updating. On listed IPR D values.
#                if ea_row[0].lower().strip() in ea_ipr_d_values \
#                        and ',' in ea_row[16]:
#                    temp_list = ea_row[16].split(',')
#                    temp_list = [x.strip() for x in temp_list]
#                    if ea_row[0].lower().strip() in temp_list:
#                        continue
#                    else:
#                        temp_list.append(ea_row[0].lower().strip())
#                        temp_dict_override.update({key: temp_list})
#                        import_override.append([ea_row[15].strip(),
#                                                ea_row[1].strip(),
#                                                ea_row[14].strip(),
#                                                temp_dict_override])
#                        continue

                # Builds dataset for non-listed values. Final Step.
                # If key not in ddi data and src value is not none.
                # Assign to merge.
                if key not in ddi_data[ddi_index][ea_row[1]]['extattrs'] \
                        and ea_row[value] not in ['', 'DDI']:
                    import_merge.append([ea_row[15].strip(),
                                         ea_row[1].strip(),
                                         ea_row[14].strip(),
                                         {key: ea_row[value]}])
                    continue
                # Checks diff against src value and a populated value in the
                # ddi data and replaces with src value.
                if ea_row[value] != \
                        ddi_data[ddi_index][
                            ea_row[1]]['extattrs'][key]['value']:
                    import_override.append([ea_row[15],
                                            ea_row[1],
                                            ea_row[14],
                                            {key: ea_row[value]}])
                    continue

    # Local scope variables.
    import_add = []
    import_delete = []
    import_merge = []
    import_override = []
    import_merge_disposition = []
    unused_list = []
    errored_list = []
    # Check for extensible attribute in Disposition column[0].
    # If found and IPR D column is empty append for writing.
    ea_ipr_d_values = ['leaf', 'dup', 'followup', 'decom', 'adv', 'divest',
                       'ignore', 're-ip', 'parent', 'drop reserve']
    _add_and_del()
    _ea_in_disposition_col0_and_empty_ipr_d_col()
    _comment_check()
    _non_listed_ea_columns_check()
    _listed_ea_column_check()
    return import_add, \
        import_delete, \
        import_merge_disposition, \
        import_merge, \
        import_override


def api_call_network_views(view, logger):
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
                logger.warning('Container View Retry #%s ,$%s', view, iview)
                time.sleep(5)
                continue
            else:
                logger.info('Timeout Error for container view: %s, %s, %s',
                            view, iview, nerrt)
                return []
    return json.loads(rnet.content.decode('utf-8'))


def api_call_networkcontainer_views(view, logger):
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
                logger.warning('Container View Retry #%s ,$%s', view, inview)
                time.sleep(5)
                continue
            else:
                logger.info('Timeout Error for container view: %s, %s, %s',
                            view, inview, cerrt)
                return []
    return json.loads(rnetcont.content.decode('utf-8'))


def get_ea_attributes(path, logger):
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
        logger.error("Can't reach IPAM! Check your VPN or Local Access, %s",
                     eaerrt)
        exit()
    except requests.exceptions.HTTPError as eahrrt:
        logger.error("Check your credentials! %s", eahrrt)
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
    logger.info("Getting EA Attributes from DDI.")
    get_ea_attributes(ea_path, logger)

    # Pull down fresh copy of view data
    ddi_data = []
    for view in net_views:
        if not view:
            continue
        logger.info("Getting data for view: %s", view)
        ddijsonnet = api_call_network_views(view, logger)
        ddijsonnetcont = api_call_networkcontainer_views(view, logger)
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


def _get_views(work_sheet):
    """Builds a set list of views from within src_ws"""
    ddi_view_col = work_sheet.row_values(0).index('DDI View')
    view_col = list(set(work_sheet.col_values(ddi_view_col)[1:]))
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
                            'Book1 vJE.xlsx')
    ea_data_file = os.path.join(raw_data_path, 'ea_data.pkl')
    ddi_data_file = os.path.join(raw_data_path, 'ddi_data.pkl')
    add_file = os.path.join(reports_data_path, 'Add Import.csv')
    merge_file = os.path.join(reports_data_path, 'Merge Import.csv')
    disposition_file = os.path.join(reports_data_path,
                                    'Merge Disposition Import.csv')
    delete_file = os.path.join(reports_data_path, 'Delete Import.csv')
    override_file = os.path.join(reports_data_path, 'Override Import.csv')

    logger.info('Loading Data from source file')
    src_wb = open_workbook(src_file)
    src_ws = src_wb.sheet_by_index(0)

    logger.info('Compiling source file list of views.')
    views = _get_views(src_ws)

    # Update to True if a fresh set of data is needed from ddi.
    ddi_api_call = False
    if ddi_api_call:
        logger.info('ddi_api_call has been set to True.  Querying DDI.')
        get_ddi_ip_data(views, ea_data_file, ddi_data_file, logger)

    def clean_data(data):
        """Build listed dataset from worksheet."""
        src_list = []
        no_net_view = []
        for row in range(data.nrows):
            # Ignore header row.
            if row == 0:
                continue
            # Ignore blank row.
            if data.row_values(row)[1] == '' and \
                    data.row_values(row)[15] == '':
                continue
            # Capture lines that do not have a view listed.
            if data.row_values(row)[1] and not data.row_values(row)[15]:
                no_net_view.append(data.row_values(row))
                continue
            src_list.append(data.row_values(row))

        # Clean's src_list values.
        src_list = [[item.replace('\t', '') for item in row
                     if isinstance(item, str)]
                    for row in src_list]
        src_list = [[item.replace('\n', ', ') for item in row
                     if isinstance(item, str)]
                    for row in src_list]
        src_list = [[item.replace(', ,', ', ') for item in row
                     if isinstance(item, str)]
                    for row in src_list]
        src_list = [[item.strip() for item in row
                     if isinstance(item, str)]
                    for row in src_list]
        for enum, row in enumerate(src_list):
            row[0] = row[0].lower()
            src_list[enum] = row
        return src_list

    src_data = clean_data(src_ws)

    # Open DDI data compiled from ddi_api_call.
    with open(ddi_data_file, 'rb') as file_in:
        ddi_data = pickle.load(file_in)
    # Build data extensions for later processing.
    views_index = _get_view_index(views, ddi_data)
    ddi_data = _get_rekey_ddi_data(ddi_data)
    ea_index = _get_ea_index()

    # Building data sets for in preparation for writing.
    add, delete, disposition, merge, override = \
        _get_diff_data(views_index, src_data, ea_index, ddi_data)

    # Send data off to be written.
    logger.info('Writing Data.  Please refer to the reports dir.')
    if add:
        _write_output_for_add_csv(add, add_file)
    if merge:
        _write_output_for_merge_csv(merge, merge_file)
    if delete:
        _write_output_for_delete_csv(delete, delete_file)
    if override:
        _write_output_for_override_csv(override, override_file)
    if disposition:
        _write_output_for_merge_disposition_csv(disposition, disposition_file)


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

    main()
