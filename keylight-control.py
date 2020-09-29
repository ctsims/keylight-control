from zeroconf import ServiceBrowser, Zeroconf
from interface import KeyLightControlPoint
import argparse
import time
import sys

class ServiceListener:

    def __init__(self, actions):
        self.actions = actions

    def remove_service(self, zeroconf, type, name):
        return

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        addr = ".".join("%d" % d for d in info.addresses[0])
        port = 9123
        self.lights = KeyLightControlPoint(addr, port)
        self.lights.load_state()
        self.trigger_actions()

    def trigger_actions(self):
        if self.actions.ptoggle:
            self.lights.set_onoff(not self.lights.is_on())

        self.lights.broadcast()
        print("Light Control Set")

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ptoggle', action='store_true')
    return parser

def main(argv):
    actions = get_parser().parse_args()

    zeroconf = Zeroconf()
    try:
        listener = ServiceListener(actions)
        browser = ServiceBrowser(zeroconf, "_elg._tcp.local.", listener)

        time.sleep(1)
    finally:
        zeroconf.close()
    

if __name__ == "__main__":
    main(sys.argv)

