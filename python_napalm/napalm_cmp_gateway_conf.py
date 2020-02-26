#!/usr/bin/env python3
from napalm import get_network_driver
import re

gateway1_ip = ''
gateway1_username = ''
gateway1_password = ''
gateway1_expertpwd = ''
gateway2_ip = ''
gateway2_username = ''
gateway2_password = ''
gateway2_expertpwd = ''

def run() -> None:
    """
        connects to hosts gateway1 & gateway2 enters expert mode,
        fetches config and compares configuration against each other
    :return: None
    """
    driver = get_network_driver('gaiaos')
    output_stripped_gwa, output_stripped_gwb = [], []
    # get config from gateway a
    device = driver(gateway1_ip, gateway1_username, gateway1_password, optional_args={'secret': gateway1_expertpwd})
    device.open()
    device.send_expert_cmd('clish -c "lock database override"')
    output_gateway_a = device.send_expert_cmd('clish -c "show configuration"')
    device.close()
    # remove comments
    regex = r'^#.*|$'
    output_gw_a = str(output_gateway_a).split(('\n'))
    for line in output_gw_a:
        if re.match(regex, line) is None:
            output_stripped_gwa.append(line)
    # get config from gateway b
    device = driver(gateway2_ip, gateway2_username, gateway2_password, optional_args={'secret': gateway2_expertpwd})
    device.open()
    device.send_expert_cmd('clish -c "lock database override"')
    output_gateway_b = device.send_expert_cmd('clish -c "show configuration"')
    device.close()
    # remove comments
    output_gw_b = str(output_gateway_b).split(('\n'))
    for line in output_gw_b:
        if re.match(regex, line) is None:
            output_stripped_gwb.append(line)
    # compare a with b
    diff_a = [x for x in output_stripped_gwa if x not in output_stripped_gwb]
    # compare b with a
    diff_b = [x for x in output_stripped_gwb if x not in output_stripped_gwa]
    #
    print('configlines on gateway1 not found on gateway2\n\n')
    for line in diff_a:
        print(line + '\n')
    print('\n\n')
    print('configlines on gateway2 not found on gateway1\n\n')
    for line in diff_b:
        print(line + '\n')
    print('\n\n')


if __name__ == '__main__':
    run()
