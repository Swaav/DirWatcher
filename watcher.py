"""Author: Swavae Miller with help from Piero and Zach"""
# TODO: create functions to track
# TODO: add try and except statements and maybe unit testing?
import logging
import datetime
import time
import argparse
import os
import signal
# below lets create the logger for the function
logger = logging.getLogger(__file__)
# ps aux | grep dirwatcher
# Use grep to use the thing, then use kill -s SIGTERM NUMBERFROMGREP
watch_files = {}
exit_flag = False
last_position = 0
def watch_directory(args):
    global watch_files
    directory = args.path
    # Keys are actual file name, and values are where to begin searching
    time.sleep(args.interval)
    file_list = [os.path.join(directory, f)
                 for f in os.listdir(directory)]
    # logger.info('Found directory {}'.format(args.path))
    for file in file_list:
        if file not in watch_files and file.endswith(args.ext):
            watch_files[file] = 0
            logger.info('Watching new file: {}'.format(file))
    for file in list(watch_files):
        if file not in file_list:
            logger.info('Removed deleted file: {}'.format(file))
            del watch_files[file]
    for file in watch_files:
        last_line_number = find_magic(
            file, watch_files[file], args.magic)
        watch_files[file] = last_line_number
    # Iterate through directionary and open files
    # See if files contain the magic text
    # Log the last position you read from the dictionary


def find_magic(filename, skip_to_line, magic_word):
    i = 0
    line = 0
    with open(filename) as f:
        for i, line in enumerate(f.readlines(), line + 1):
            if i <= skip_to_line:
                continue
            if magic_word in line:
                logger.info('Found the {} on {} in {}'
                            .format(magic_word, i, filename))
        # Returns the last value which was read
    return i


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='How often to watch the text file')
    parser.add_argument('path', help='Directory to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser
def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be
    mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's
    loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    logger.warning('Received ' + signal.Signals(sig_num).name)
    # log the signal name (the python2 way)
    # signames = dict((k, v) for v, k in reversed(
    #     sorted(signal.__dict__.items()))
    #     if v.startswith('SIG') and not v.startswith('SIG_'))
    # logger.warn('Received ' + signames[sig_num])
    global exit_flag
    exit_flag = True
def main():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '----------------------------------------------------\n'
        '   Running {0}\n'
        '   Started on {1}\n'
        '----------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    logger.info('Watch Dir: {}, File Ext: {}, Polling Int: {}, Magic Txt: {}'
                .format(args.path, args.ext, args.interval, args.magic))
    while not exit_flag:
        try:
            watch_directory(args)
        except OSError as e:
            logger.error('Directory not found: {}'.format(args.path))
            time.sleep(5.0)
        except Exception as e:
            logger.error('Unhandled exception: {}'.format(e))
            time.sleep(5.0)
        # except KeyboardInterrupt:
        #     break
            # put a sleep inside my while loop so
            # I don't peg the cpu usage at 100%
    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start.
    uptime = datetime.datetime.now() - app_start_time
    logger.info(
        '\n'
        '----------------------------------------------------\n'
        '   Stopped {0}\n'
        '   Uptime was {1}\n'
        '----------------------------------------------------\n'
        .format(__file__, str(uptime))
    )
if __name__ == '__main__':
    main()
