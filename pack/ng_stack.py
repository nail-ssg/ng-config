from collections import OrderedDict
from copy import deepcopy


def is_dict(obj):
    return isinstance(obj, dict) or isinstance(obj, OrderedDict)


class Layer(OrderedDict):
    """docstring for Layer"""

    def __init__(self, layer, name=None):
        new_layer = deepcopy(dict(layer))
        super(Layer, self).__init__(new_layer)

    def _modify(self, obj, value):
        for key in value:
            if len(key) > 2 and key[:2] == '-!':
                key_ = key[2:]
                if key_ in self:
                    del obj[key_]
            elif len(key) > 2 and key[-2:] == '!-':
                key_ = key[:-2]
                if key_ in obj:
                    sub_obj = obj[key_]
                    sub_value = value[key]
                    if (isinstance(sub_obj, list) or is_dict(sub_obj)) and isinstance(sub_value, list):
                        for item in sub_value:
                            if item in sub_obj:
                                sub_obj.remove(item)
            elif key in obj and key in value:
                sub_obj = obj[key]
                sub_value = value[key]
                if (isinstance(sub_obj, list) or is_dict(sub_obj)) and isinstance(sub_value, list):
                    for item in sub_value:
                        if item[:2] != '-!': continue
                        key_ = item[2:]
                        if key_ in sub_obj:
                            if isinstance(sub_obj, list):
                                sub_obj.remove(key_)
                            else:
                                del sub_obj[key_]
        if not is_dict(obj):
            return
        if is_dict(value):
            for key in value:
                if len(key) > 2 and ('-!' == key[:2] or '!-' == key[-2:]):
                    continue
                elif key in obj:
                    sub_obj = obj[key]
                    sub_value = value[key]
                    if is_dict(sub_obj) and is_dict(sub_value):
                        self._modify(sub_obj, sub_value)
                    elif isinstance(sub_obj, list) and isinstance(sub_value, list):
                        for item in sub_value:
                            if len(item) > 2 and '-!' == item[:2]:
                                continue
                            sub_obj += [item]
                    elif is_dict(sub_obj) and isinstance(sub_value, list):
                        pass
                    else:
                        obj[key] = sub_value
                else:
                    obj[key] = value[key]

    def __add__(self, value):
        if not is_dict(value):
            raise Exception('Ups')
        result = Layer(self)
        self._modify(result, value)
        return result


class Stack(object):
    """docstring for Stack"""
    _last_id = 0
    _final_layer = None

    def __init__(self):
        super(Stack, self).__init__()
        self._layers = {}
        self._layer_order = []
        self._final_layer = Layer({})
        self._assemble()

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
