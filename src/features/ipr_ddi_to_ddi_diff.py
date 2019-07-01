"""Performs a diff and outputs the information for use by the import
generator script."""
import os
import logging
from xlrd import open_workbook
from openpyxl import Workbook
from dotenv import find_dotenv, load_dotenv


def _write_output_to_master(diff_list, output_file):
    """Write Output"""
    w_b = Workbook()
    w_s = w_b.active
    w_s.title = 'IPR_Diff'
    for row_indx, stuff in enumerate(diff_list):
        for col_indx, item in enumerate(stuff):
            w_s.cell(row=row_indx+1, column=col_indx + 1, value=item)
    w_b.save(output_file)


def main():
    """Script that takes in two .xlsx files in IPR format.  Performs a diff
    against them and generates an output .xlsx file."""
    logger = logging.getLogger('ipr_ddi_to_ddi_diff.py')
    logger.info('Beginning of Script')
    logger.info('Building Paths and Filenames')
    # Build path's.
    interim_data_path = os.path.join(PROJECT_DIR, 'data', 'interim')
    processed_data_path = os.path.join(PROJECT_DIR, 'data', 'processed')

    # Join file names to path's.
    ipr_src_file = os.path.join(interim_data_path,
                                'DDI_to_IPR 20190607.xlsx')
    ipr_src_mod_file = os.path.join(interim_data_path,
                                    'IPAM-to-IPR-2019-06-27.xlsx')
    output_file = os.path.join(processed_data_path,
                               'Diff between 0607 and 0627 Master.xlsx')

    logger.info('Loading Data')
    # Original Dataset Check Sheet index
    ipr = open_workbook(ipr_src_file)
    ipr_sheet = ipr.sheet_by_index(0)
    # Modified Dataset Check Sheet index
    ipr_mod = open_workbook(ipr_src_mod_file)
    ipr_mod_sheet = ipr_mod.sheet_by_index(0)

    # Add Datasets to a python list.
    updatelist = []
    updatelist.append(HEADER_ROW[0:17])
    ipr_data = []
    ipr_mod_data = []
    for enum in range(ipr_sheet.nrows):
        ipr_data.append(ipr_sheet.row_values(enum)[0:17])
    for enum in range(ipr_mod_sheet.nrows):
        ipr_mod_data.append(ipr_mod_sheet.row_values(enum)[0:17])

    logger.info('Building Diff List from modified file.')
    # Build Diff List for processing.
    for enum, ipr_mod_row in enumerate(ipr_mod_data):
        if ipr_mod_row[0] == 'self-overlap':
            continue
        # if ipr_mod_row[0] == 'del':
        #    continue
        if enum == 0:
            continue
        if ipr_mod_row not in ipr_data:
            updatelist.append(ipr_mod_row)
            continue
    logger.info('Writing output.')
    _write_output_to_master(updatelist, output_file)
    logger.info('Script Complete: Refer to data\\processed')


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
