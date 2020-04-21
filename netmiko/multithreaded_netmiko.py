import asyncio
import concurrent.futures
import logging
import sys
import collections
from netmiko import ConnectHandler

# ! read from bottom !

# here we define what we want to do on the device, the logging stuff is eye candy 
def execute_remote_job(target_host, username, password, secret, device_type):
    log = logging.getLogger('connecting to ({})'.format(target_host))
    log.info('running')
    # here we assign the parameters for the target system
    device = {'device_type': device_type, 'host': target_host, 'username': username, 'password': password, 'secret' : secret }
    # lazy exception handling - assume it fails and only change if it works.
    output = 'connection failed'
    try:
        # we fetch show run here
        # commands are obviously platform dependent
        # this example applies to cisco ios. commands might differ 
        log.info('connect')
        # open ssh connection to device and pass keyword arguments as dict
        # the double-* indicates that argument expansion is used
        net_connect = ConnectHandler(**device)
        log.info('find prompt')
         # get prompt bevor sending a command
        net_connect.find_prompt()
        log.info('set term 0')
        # set number of lines bevor pausing output on cisco ios to 0 (no pause)
        net_connect.send_command('terminal length 0') 
        net_connect.find_prompt()
        # and here we send sh run and assign answer to output
        log.info('fetch conf')
        output = net_connect.send_command("show run")
        log.info('done')
    except:
        log.info('failed')
        pass
    return output


async def run_remote_jobs(executor):
 
    # here we define the device-lists and spawn the threads - we will separate this in later incarnations (tbd) 
    log = logging.getLogger('run remote-jobs')
    log.info('starting')
    # device list is simply a dictionary
    devices = {'sw1' :
                    {'ip': 'X.X.X.X',
                     'type': 'cisco_ios',
                     'user': 'uid',
                     'password': 'pwd',
                     'secret': 'secret'}}
    # we require an ordered dict for the iteration within blocking tasks
    devices = collections.OrderedDict(devices)
    log.info('creating remote jobs')
    loop = asyncio.get_event_loop()
    # run in executor does not support argument expansion, therefore use separate params
    blocking_tasks = [
        loop.run_in_executor(executor,
                             execute_remote_job,
                             devices[device]['ip'],
                             devices[device]['user'],
                             devices[device]['password'],
                             devices[device]['secret'],
                             devices[device]['type'] 
        )
        for device in devices
    ]
    log.info('waiting for executor tasks')
    # here we write our results into futures(implicit)
    completed, pending = await asyncio.wait(blocking_tasks)
    # we could use a loop aswell, but list comprehension is way more pythonic(and faster)
    results = [t.result() for t in completed]
    # let's see what we got -  this is asynchronous and will be triggered when a task is completed
    log.info('results: {!r}'.format(results))
    


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
    # use asyncio threadexecutor within asyncio main loop
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_remote_jobs(executor)
        )
    finally:
        event_loop.close()
