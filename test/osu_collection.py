# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import vlq_base128_le
class OsuCollection(KaitaiStruct):
    """collection.db file format in rhythm game, osu!.
    
    .. seealso::
       Source - https://osu.ppy.sh/wiki/zh-tw/osu%21_File_Formats/Db_%28file_format%29
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.version = self._io.read_s4le()
        self.num_collections = self._io.read_s4le()
        self.collections = [None] * (self.num_collections)
        for i in range(self.num_collections):
            self.collections[i] = OsuCollection.Collection(self._io, self, self._root)


    class Collection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = OsuCollection.String(self._io, self, self._root)
            self.num_beatmaps = self._io.read_s4le()
            self.beatmaps_md5s = [None] * (self.num_beatmaps)
            for i in range(self.num_beatmaps):
                self.beatmaps_md5s[i] = OsuCollection.String(self._io, self, self._root)



    class String(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.is_present = self._io.read_s1()
            if self.is_present == 11:
                self.len_str = vlq_base128_le.VlqBase128Le(self._io)

            if self.is_present == 11:
                self.value = (self._io.read_bytes(self.len_str.value)).decode(u"UTF-8")




