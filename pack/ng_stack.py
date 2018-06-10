from collections import UserDict
from copy import deepcopy


class Layer(UserDict):
    """docstring for Layer"""

    def __init__(self, layer, name=None):
        layer_dict = deepcopy(layer)
        super(Layer, self).__init__(layer_dict)

    def _modify(self, obj, value):
        for key in value:
            if not key:
                continue
            if key[0] == '-':
                key_ = key[1:]
                if key_ in self:
                    del obj[key_]
        for key in value:
            if not key:
                continue
            if key[0] == '-':
                continue
            if key in obj:
                print('k: ', key)
                print(' obj: ', obj)
                print(' val: ', value)
                if (isinstance(obj, dict) or isinstance(obj, UserDict)) and isinstance(value, dict):
                    print('ok')
                    self._modify(obj[key], value[key])
            else:
                obj[key] = value[key]

    def __add__(self, value):
        if not isinstance(value, Layer) and not isinstance(value, dict):
            raise Exception('Ups')
        result = Layer(self)
        self._modify(result, value)
        return result


class Stack(object):
    """docstring for Stack"""
    _layers = {}
    _layer_order = []
    _last_id = 0
    _final_layer = None

    def __init__(self):
        super(Stack, self).__init__()
        self._assemble()
        # self.arg = arg

    def _assemble(self):
        self._final_layer = Layer({})
        for id in self._layer_order:
            layer = self._layers[id]
            self._final_layer += layer

    def push(self, layer, id=None):
        while not id or id in self._layers:
            self._last_id += 1
            id = self._last_id
        if id in self._layers:
            raise Exception("use 'replace' method")
        self._layer_order += [id]
        self._layers[id] = layer
        self._final_layer += layer
        return id

    def as_dict(self):
        return dict(self._final_layer)
