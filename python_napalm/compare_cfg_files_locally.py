""" compares gaia os configs for differences """
#!/usr/bin/env python3
import sys
import re
import os

def run():
    files = _get_args()
    if files is None:
        print("Error: missing argument\nUsage: {} <file1> <file1>".format(os.path.basename(__file__)))
        sys.exit(1)
    cfgdata = read_files(*files)
    compare_config(cfgdata, files)

def _get_args():
    try:
        return (sys.argv[1], sys.argv[2])
    except:
        return None

def read_files(file1, file2):
    regex = r'^#.*|$'
    keys = ('host_a', 'host_b')
    i = 0
    cfg_a, cfg_b = [], []
    with open(file1, 'r') as fh:
        for line in fh:
            # filter for comments and empty lines first
            if re.match(regex, line) is None:
                cfg_a.append(line)
    with open(file2, 'r') as fh:
        for line in fh:
            # filter for comments and empty lines first
            if re.match(regex, line) is None:
                cfg_b.append(line)
    return (cfg_a, cfg_b)

def compare_config(cfgdata, files):
    ln = '-' * 80
    diff_a = [x for x in cfgdata[0] if x not in cfgdata[1]]
    diff_b = [x for x in cfgdata[1] if x not in cfgdata[0]]
    print('configlines in {} not found in {}\n\n'.format(files[0], files[1]))
    print('{}'.format(ln))
    for line in diff_a:
        print(line)
    print('\n\n{}\n'.format(ln))
    print('configlines in {} not found in {}\n\n'.format(files[1], files[0]))
    for line in diff_b:
        print(line)
    print('\n\n{}\n'.format(ln))

if __name__ == '__main__':
    run()
