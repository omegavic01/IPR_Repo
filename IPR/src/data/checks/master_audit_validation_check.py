"""IP Validation check.  Fundamental checks for:

    1. Whether or not a cidr is listed within the cidr field.
    2. Cidr blocks larger than a /13
    3. Leading zero's within network ip address.
    4. Checks for a valid Network Address.
"""
import os
import ipaddress
import re
import logging


def out_log(loggs, logfile):
    """Updates log file:

        Log File name:
        -- validation check log.txt
    """
    with open(logfile, 'w') as file:
        for log in loggs:
            file.write(log)
            file.write('\n')


def validation_check(check, logfile):
    """Performs the following actions:

    1. Checks to make sure there is a "/" within network address.
    2. Checks for leading zero's within each octet of the network address.
    3. Checks to see if the network address has host bits set.

    Creates a log and updates the following arg for logfile creation:

    Argument:
    -- erroredlist
    """
    error_list = []
    for item in check:
        _ip = item[0].value
        if _ip == 'CIDR':
            continue
        if '/' not in _ip:
            error_list.append(str(_ip + ' does not appear to contain a CIDR'))
            continue
        if int(_ip.strip().split('/')[1]) not in list(range(13, 33)):
            error_list.append(str(_ip + ' out of range CIDR'))
            continue
        # if not re.match(regex, str(ip.strip().split('/')[0])):
        #    erroredlist.append(str(ip + ' Failed Regex Match'))
        #    continue
        octets = re.findall(r"[\d']+", _ip)
        leadzerostate = ""
        for octs in octets:  # Beggining check for lead zero
            if len(octs) > 1 and octs.startswith('0'):
                leadzerostate = True
                break
        if leadzerostate:
            octets[:] = [str(int(x)) for x in octets]
            octets[3:] = ['/'.join(octets[3:])]
            new_octets = '.'.join(octets[:])
            error_list.append(str(_ip +
                                  " Leading zero's in IP please update to: " +
                                  new_octets))
        try:
            if ipaddress.ip_network(_ip.strip()):
                pass
        except ValueError as err:
            error_list.append(str(err).replace("'", ""))

    for index, i in enumerate(error_list):
        if 'has host bits set' in i:
            error_list[index] = i + ' Network is: ' + \
                             str(ipaddress.IPv4Interface((i.strip()).split(' ')
                                                         [0]).network)
            continue
    if error_list:
        out_log(error_list, logfile)
        return 'Unclean'
    return True


if __name__ == '__main__':
    # getting root directory
    PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # setup logger
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)
