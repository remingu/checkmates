import asyncio
import concurrent.futures
import logging
import sys
import collections
from netmiko import ConnectHandler


def execute_remote_job(host1):
    log = logging.getLogger('connecting to ({})'.format(host1))
    log.info('running')
    device = {'device_type': 'cisco_s300', 'host': '192.168.10.253', 'username': 'cisco', 'password': 'cisco'}
    output = 'connection failed'
    try:
        log.info('connect')
        net_connect = ConnectHandler(**device)
        log.info('find prompt')
        net_connect.find_prompt()
        log.info('set term len 0')
        net_connect.send_command('terminal length 0')
        log.info('fetch conf')
        output = net_connect.send_command("show run")
        log.info(output)
        log.info('done')
    except:
        log.info('failed')
        pass
    return output


async def run_remote_jobs(executor):
    log = logging.getLogger('run remote-jobs')
    log.info('starting')
    devices = {'sw1' :
                    {'ip' : '192.168.10.253',
                     'type' : 'cisco_s300' ,
                     'user' : 'cisco',
                     'password' : 'cisco',
                     'secret' : 'secret'}}
    devices = collections.OrderedDict(devices)
    log.info('creating remote jobs')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, execute_remote_job, 'something')
        for device in devices
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))
    log.info('exiting')


if __name__ == '__main__':
    # Configure logging to show the name of the thread
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited thread pool.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=8,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_remote_jobs(executor)
        )
    finally:
        event_loop.close()