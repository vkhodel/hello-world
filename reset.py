#!/usr/bin/python
# ping 8.8.8.8 in a loop
# on success
#   sleep 60
# on failure
#   power cycle modem
#   don't do this continuously, just cover two use cases:
#   -modem malfunction/memory leak - p/cycle and check
#   -network outage - p/cycle and keep trying over increasing interval
#   so check every minute, but p/cycle like this:
#   1, 2, 4, 8, 16, 32, 64
import os
import time


PING_TARGET = '8.8.8.8'

PING_OK_INTERVAL = 2
#PING_OK_INTERVAL = 60

BACKOFF_EXPONENT = 2
# let's back off to at most 60 minutes
MAX_BACKOFF_STEPS = 5
MAX_BACKOFF_INTERVAL = PING_OK_INTERVAL * pow(BACKOFF_EXPONENT, MAX_BACKOFF_STEPS)


def ping_ok():
    print('Ping...')
    #os.system('ping -s %s' % PING_TARGET)
    # two test scenarios
    # occasional failure
    return int(time.time()) % 5 == 0
    # long continuous failure


def reset_modem():
    print('Resetting modem...')


def main():
    backoff_interval = PING_OK_INTERVAL
    success_timestamp = time.time()
    reset_timestamp = success_timestamp

    while True:
        if ping_ok():
            print('  Ping ok!')
            # reset backoff counter
            backoff_interval = PING_OK_INTERVAL
            success_timestamp = time.time()
            reset_timestamp = success_timestamp
        else:
            print('  Ping failed!')
            # ping failed, reset modem if outside of backoff interval
            if time.time() > reset_timestamp + backoff_interval:
                reset_modem()
                reset_timestamp = time.time()
                if backoff_interval < MAX_BACKOFF_INTERVAL:
                    backoff_interval *= BACKOFF_EXPONENT
                    print('    Increased backoff interval to %d' % backoff_interval)
            else:
                print('  Waiting to reset modem: %s < %s' % (
                    time.time() - reset_timestamp, backoff_interval))

        time.sleep(PING_OK_INTERVAL)
 

if __name__ == '__main__':
    main()
