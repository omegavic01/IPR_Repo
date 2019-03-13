"""
Script used to call the five scripts needed to generate the reports requested
by IPR.
"""
import logging
import os
import sys


def main():
    """
    Main Wrapper function that builds the path and has the filenames listed.
    Then to execute the scripts one by one.
    """
    logger = logging.getLogger(sys.argv[0].split('/')[-1])
    logger.info('Beginning of Script')
    # Build path's.
    src_data_path = os.path.join(PROJECT_DIR, 'src', 'data')
    src_features_path = os.path.join(PROJECT_DIR, 'src', 'features')

    # Join file names to path's.
    step_one_ipam_query = os.path.join(src_data_path,
                                       'ipr_initial_data_gathering.py')
    step_two_ddi_to_master = os.path.join(src_data_path,
                                          'ipr_format_ddi.py')
    step_three_master_audit = os.path.join(src_data_path,
                                           'ipr_audit_ddi.py')
    step_four_vrf_check = os.path.join(src_features_path,
                                       'ipr_clean_vrf_check.py')
    step_five_report_percent = os.path.join(src_features_path,
                                            'ipr_report_percent.py')
    exec(open(step_one_ipam_query).read(), globals())
    exec(open(step_two_ddi_to_master).read(), globals())
    exec(open(step_three_master_audit).read(), globals())
    exec(open(step_four_vrf_check).read(), globals())
    exec(open(step_five_report_percent).read(), globals())


if __name__ == '__main__':
    # getting root directory
    PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # setup logger
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    main()
