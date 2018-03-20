class Layer(object):
    """docstring for Layer"""

    def __init__(self, layer_dict, name=None):
        assert type(layer_dict) == dict, ""
        super(Layer, self).__init__()
        self._layer_dict = layer_dict


class Stack(object):
    """docstring for Stack"""

    def __init__(self):
        super(Stack, self).__init__()
        # self.arg = arg

    def push(layer, id):
        return id

    def as_dict():
        return {}
