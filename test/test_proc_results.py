"""Test module for process_results function in awss."""

import awss.debg as debg
from awss.core import process_results

from awsrawdata import rawdata

expected_info = {
    0: {'ami': 'ami-3d3a6b78',
        'id': 'i-04a10a9a89f05523d',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'Fedora',
                'Project': 'SysAdmin',
                'Role': 'Regression',
                'Team': 'Dev10a'}}}


def test_process_results():
    """Test process of converting raw data to i_info."""

    debg.init(False, False)

    ret_info = process_results(rawdata)

    assert ret_info[0]['id'] == expected_info[0]['id']
    assert ret_info[0]['state'] == expected_info[0]['state']
    assert ret_info[0]['ami'] == expected_info[0]['ami']
    assert ret_info[0]['ssh_key'] == expected_info[0]['ssh_key']
    assert ret_info[0]['pub_dns_name'] == expected_info[0]['pub_dns_name']
    assert ret_info[0]['tag'] == expected_info[0]['tag']
