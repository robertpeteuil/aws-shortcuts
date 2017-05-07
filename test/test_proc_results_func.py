"""Test module for process_results function in awss."""

import pytest
import awss.debg as debg
from awss.core import process_results

# import raw query data returned from AWS
from awsresponse import rawdata, rawdata_nt, rawdata_term

# import expected info extracted from raw data
from awsstestdata import expected_info, expected_info_nt, expected_info_term


@pytest.mark.parametrize(("inputdata", "resultdata"), [
    (rawdata, expected_info),
    (rawdata_nt, expected_info_nt),
    (rawdata_term, expected_info_term)])
def test_process_results(inputdata, resultdata):
    """Test process of converting raw data to i_info."""

    debg.init(False, False)

    ret_info = process_results(inputdata)

    assert ret_info[0]['id'] == resultdata[0]['id']
    assert ret_info[0]['state'] == resultdata[0]['state']
    assert ret_info[0]['ami'] == resultdata[0]['ami']
    assert ret_info[0]['ssh_key'] == resultdata[0]['ssh_key']
    assert ret_info[0]['pub_dns_name'] == resultdata[0]['pub_dns_name']
    assert ret_info[0]['tag'] == resultdata[0]['tag']
