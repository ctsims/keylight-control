import requests

class KeyLightControlPoint:

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
    
    def load_state(self):
        r = requests.get("http://%s:%s/elgato/lights" % (self.addr, self.port))
        if not r.status_code == 200:
            raise Exception("Bad control response %d" % r.status_code)
        self.state = r.json()
        print("Light discovered")

    def set_onoff(self, isOn):
        for light in self.state['lights']:
            light['on'] = 1 if isOn else 0

    def is_on(self):
        for light in self.state['lights']:
            if light['on'] == 1:
                return True

        return False
    
    def broadcast(self):
        r = requests.put("http://%s:%s/elgato/lights" % (self.addr, self.port), json=self.state)
        if not r.status_code == 200:
            raise Exception("Invalid response to PUT %d" % r.status_code)
