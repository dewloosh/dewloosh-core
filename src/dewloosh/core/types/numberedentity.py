# -*- coding: utf-8 -*-
from abc import ABC
import uuid

__all__ = ['Numbered', 'Unique']


class Numbered(ABC):

    def __init__(self, *args, num=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.num = num

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass

    def __eq__(self, other):
        return self.num == other.num


class Unique(ABC):

    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        if 'UUID' in kwargs:
            UUID = kwargs.pop('UUID')
        elif 'UID' in kwargs:
            UUID = kwargs.pop('UID')
        else:
            UUID = uuid.uuid4()

        if 'GUID' in kwargs:
            GUID = kwargs.pop('GUID')
        elif 'GID' in kwargs:
            GUID = kwargs.pop('GID')
        else:
            GUID = None

        if 'ID' in kwargs:
            ID = kwargs.pop('ID')
        elif 'LID' in kwargs:
            ID = kwargs.pop('LID')
        else:
            ID = None

        self._UUID = UUID
        self._ID = ID
        self._GUID = GUID
        self._key = key

    def __eq__(self, other):
        return isinstance(other, Unique) and self.UUID == other.UUID

    @property
    def to_hex(self):
        return self.UUID.hex

    @property
    def to_int(self):
        return self.UUID.int

    @property
    def GUID(self):
        return self._GUID

    @GUID.setter
    def GUID(self, value):
        self._GUID = value

    @property
    def GID(self):
        return self._GUID

    @GID.setter
    def GID(self, value):
        self._GUID = value

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @property
    def LID(self):
        return self._ID

    @LID.setter
    def LID(self, value):
        self._ID = value

    @property
    def UUID(self):
        return self._UUID

    @property
    def UID(self):
        return self._UUID

    def __hash__(self):
        return self.to_int()

    @property
    def key(self):
        return self._key if self._key is not None else self._UUID

    @key.setter
    def key(self, value):
        self._key = value

    def __str__(self):
        return str(self.key)


class UniqueNumbered(Numbered, Unique):
    ...


if __name__ == '__main__':

    u1 = UniqueNumbered()
    u2 = UniqueNumbered(key='somekey')
