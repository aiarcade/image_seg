class Map(dict):
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

class CustomParser(object):
    def __init__(self):
        self.config={}
    def add_argument(self,flag,type,default,help=None):
        key=flag.replace("--","")
        if type==float:
            value=float(default)
        if type==str:
            value=str(default)
        if type==int:
            value=int(default)
        self.config[key]=value
    def parse_args(self):
        return Map(self.config)

