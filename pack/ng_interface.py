from abc import ABC, abstractmethod
from collections import UserList

_types = {}


class TypeMixin(ABC):
    type_name = ''
    type_description = ''

    def __init__(self):
        if not self.type_name:
            self.type_name = self.__name__

    @abstractmethod
    def verify(self):
        return False


class Type(TypeMixin):
    pass


class CustomList(UserList):
    container_type = None

    def __init__(self):
        if self.container_type is None:
            Exception("Property 'container_type' is None")
        if issubclass(self.container_type, Type):
            Exception("Property 'container_type' is not Type")

    def append(self, item):
        self.container_type.verify(item)
        super().append(item)


class OneOf(CustomList):
    _index = 0

    @property
    def value(self):
        return self[self._index]

    @property
    def value_index(self):
        return self._index

    def choice(self, index):
        if index in range(len(self)):
            self._index = index
        else:
            raise IndexError()

    @value_index.setter
    def value_index(self, value):
        self.choice(value)


class ManyOf(CustomList):
    allow_empty_selected = True
    _selected_indexes = set()

    @property
    def selected(self):
        return [item for index, item in enumerate(self) if index in self._selected_indexes]

    def select(self, index):
        if index in range(len(self)):
            self._selected_indexes.add(index)
        else:
            raise IndexError()

    def unselect(self, index):
        if index in range(len(self)):
            self._selected_indexes.remove(index)
        else:
            raise IndexError()

    def set_order(self, new_order):
        if len(new_order) != len(self):
            Exception("new_order must be the same length")
        if len(set(new_order)) != len(self):
            Exception("new_order hasn't correct value")
        tmp = UserList(self)
        si = self._selected_indexes
        self.clear()
        for index, old_index in enumerate(new_order):
            if old_index in si:
                self._selected_indexes.add(index)
                self += [tmp[old_index]]

    def clear(self):
        super().clear()
        self._selected_indexes = set()

    def remove(self, item):
        i = self.index(item)
        for index, value in enumerate(self._selected_indexes):
            if value >= i:
                self._selected_indexes[index] -= 1
        super().remove(item)
