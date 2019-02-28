"""This script is intended to take in the DDI data generated from the
ipam_query_app_full_report_xls.py script.  Twist, mash, and split the data.

DataSets:
   DDI-to-IPR-Format-Unsorted.xlsx -- output file
   ddi_workbook.xls -- input file
"""
import os
import logging
from xlrd import open_workbook
from ipaddr import IPv4Network
from openpyxl import Workbook
from openpyxl.styles import Alignment
from dotenv import find_dotenv, load_dotenv


def _write_output_to_master(genop, path):
    """Write out the rows in IPR expected format.

    Output Arguments:
        output_file - DDI-to-IPR-Format-Unsorted.xlsx
    """

    work_book = Workbook()
    w_s = work_book.active  # work_sheet
    w_s.title = 'MASTER'
    row = 1
    col = 0
    for index, item in enumerate(HEADER_ROW):
        w_s.cell(row=row, column=index + 1, value=item)
    for bit in genop:
        row = row + 1
        w_s.cell(row=row, column=col + 2, value=bit[3])  # Cidr
        w_s.cell(row=row, column=col + 3, value=bit[23])  # region
        w_s.cell(row=row, column=col + 4, value=bit[15])  # country
        w_s.cell(row=row, column=col + 5, value=bit[12])  # city
        w_s.cell(row=row, column=col + 6, value=bit[7])  # address
        w_s.cell(row=row, column=col + 7, value=bit[27])  # site
        w_s.cell(row=row, column=col + 8, value=bit[16])  # datacenter
        w_s.cell(row=row, column=col + 9, value=bit[17])  # division
        w_s.cell(row=row, column=col + 10, value=bit[26])  # requester_email
        w_s.cell(row=row, column=col + 11, value=bit[8])  # agency
        w_s.cell(row=row, column=col + 13, value=bit[5])  # comment
        w_s.cell(row=row, column=col + 12, value=bit[31])  # vlandesc
        w_s.cell(row=row, column=col + 14, value=bit[19])  # interfacename
        w_s.cell(row=row, column=col + 15, value=bit[0])  # ddi_type
        w_s.cell(row=row, column=col + 16, value=bit[4])  # ddi_view
        w_s.cell(row=row, column=col + 17, value='DDI')
        mycell = w_s.cell(row=row, column=col + 18)
        mycell.alignment = Alignment(horizontal='left')
        mycell.value = int(bit[3].split('.')[0])  # first octet
        mycell = w_s.cell(row=row, column=col + 19)
        mycell.alignment = Alignment(horizontal='left')
        mycell.value = int(bit[3].split('.')[1])  # second octet
        mycell = w_s.cell(row=row, column=col + 20)
        mycell.alignment = Alignment(horizontal='left')
        mycell.value = int(bit[3].split('.')[2])  # third octet
        mycell = w_s.cell(row=row, column=col + 21)
        mycell.alignment = Alignment(horizontal='left')
        mycell.value = int(bit[3].split('.')[3].split('/')[0])  # fourth octet
        mycell = w_s.cell(row=row, column=col + 22)
        mycell.alignment = Alignment(horizontal='left')
        mycell.value = int(bit[3].split('/')[1])  # cidr for network addr.
    work_book.save(path)


def main():
    """Takes path and opens workbook.  Takes in DDI data and filters out
    unused data.  Once filtered it sends the array for writing.

    Output Arguments:
        outputddilist = list of rows from spreadsheet.
    """
    # get logger
    logger = logging.getLogger(__name__)
    logger.info('Beginning of Script')
    # Build paths and file names.
    raw_data_path = os.path.join(PROJECT_DIR, 'data', 'raw')
    interim_data_path = os.path.join(PROJECT_DIR, 'data', 'interim')
    ddi_file = os.path.join(raw_data_path, 'ddi_workbook.xls')
    interim_ddi_file = os.path.join(interim_data_path,
                                    'DDI_IPR_Unsorted.xlsx')

    # Opens ddi_workbook.xls
    rddi = open_workbook(ddi_file)
    rddifirst_sheet = rddi.sheet_by_index(0)

    logger.info('Filtering out unneeded data.')
    #  For filtering out data not needed.
    output_ddi_list = []
    for i in range(rddifirst_sheet.nrows):
        if i == 0:
            continue
        if '/32' in rddifirst_sheet.row_values(i)[2]:
            continue
        if '100.88.0.0/29' in rddifirst_sheet.row_values(i)[3]:
            continue
        if '100.64.0.0/29' in rddifirst_sheet.row_values(i)[3]:
            continue
        if 'free ip' in rddifirst_sheet.row_values(i)[5].lower() \
                and '00890' in rddifirst_sheet.row_values(i)[4]:
            continue
        if int(rddifirst_sheet.row_values(i)[2][1:3]) in range(1, 16):
            continue
        if rddifirst_sheet.row_values(i)[4] == 'Public-IP':
            continue
        if rddifirst_sheet.row_values(i)[4] == 'wan_test':
            continue
        if IPv4Network(rddifirst_sheet.row_values(i)[1]).is_private:
            output_ddi_list.append(rddifirst_sheet.row_values(i))
        elif IPv4Network(rddifirst_sheet.row_values(i)[1]).is_cgn:
            output_ddi_list.append(rddifirst_sheet.row_values(i))

    # Send information for processing and to write output.
    logger.info('Writing out DDI-to-IPR-Format-Unsorted.xlsx')
    _write_output_to_master(output_ddi_list, interim_ddi_file)
    logger.info('Script Complete')


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

    main()
