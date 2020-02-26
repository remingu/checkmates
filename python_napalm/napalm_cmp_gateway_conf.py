#!/usr/bin/env python3
from napalm import get_network_driver
import re

gateway1_ip = '192.168.10.35'
gateway1_username = 'admin'
gateway1_password = 'test12'
gateway1_expertpwd = 'test12'
gateway2_ip = '192.168.10.35'
gateway2_username = 'admin'
gateway2_password = 'test12'
gateway2_expertpwd = 'test12'

def run():
    driver = get_network_driver('gaiaos')
    output_stripped_gwa, output_stripped_gwb = [], []
    # get config from gateway a
    device = driver(gateway1_ip, gateway1_username, gateway1_password, optional_args={'secret': gateway1_expertpwd})
    device.open()
    device.send_expert_cmd('clish -c "lock database override"')
    output_gateway_a = device.send_expert_cmd('clish -c "show configuration"')
    device.close()
    # remove comments
    regex = r'#.*|$'
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
    output_stripped_gwb.clear()
    output_stripped_gwb.append('1')
    # compare a with b
    diff_a = [x for x in output_stripped_gwa if x not in output_stripped_gwb]
    # compare b with a
    diff_b = [x for x in output_stripped_gwb if x not in output_stripped_gwa]
    #
    print('config on host_a not available on host b\n\n')
    for line in diff_a:
        print(line + '\n')
    print('\n\n')
    print('config on host_b not available on host a\n\n')
    for line in diff_b:
        print(line + '\n')
    print('\n\n')

if __name__ == '__main__':
    run()