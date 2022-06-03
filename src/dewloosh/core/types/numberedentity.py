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

    def __init__(self, *args, key=None, UUID=None, UID=None, GUID=None, 
                 GID=None, ID=None, LID=None, **kwargs):
        super().__init__(*args, **kwargs)
        UID = UUID if UUID is not None else UID
        UID = UID if UID is not None else uuid.uuid4()
        self._UUID = UID
        self._ID = ID if ID is not None else LID
        self._GUID = GUID if GUID is not None else GID
        self._key = key

    def __eq__(self, other):
        return hasattr(other, 'UUID') and self.UUID == other.UUID
    
    def __hash__(self):
        return hash(self.to_int)

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

    @property
    def key(self):
        return self._key if self._key is not None else self._UUID

    @key.setter
    def key(self, value):
        self._key = value

    def __str__(self):
        return str(self.key)


class UniqueNumbered(Unique, Numbered):
    ...

