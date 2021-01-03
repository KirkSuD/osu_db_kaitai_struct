# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import vlq_base128_le
class OsuScores(KaitaiStruct):
    """scores.db file format in rhythm game, osu!.
    
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
        self.num_beatmaps = self._io.read_s4le()
        self.beatmaps = [None] * (self.num_beatmaps)
        for i in range(self.num_beatmaps):
            self.beatmaps[i] = OsuScores.Beatmap(self._io, self, self._root)


    class Bool(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.byte = self._io.read_s1()

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value if hasattr(self, '_m_value') else None

            self._m_value = (False if self.byte == 0 else True)
            return self._m_value if hasattr(self, '_m_value') else None


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



    class Beatmap(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.md5_hash = OsuScores.String(self._io, self, self._root)
            self.num_scores = self._io.read_s4le()
            self.scores = [None] * (self.num_scores)
            for i in range(self.num_scores):
                self.scores[i] = OsuScores.Score(self._io, self, self._root)



    class Score(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.gameplay_mode = self._io.read_s1()
            self.version = self._io.read_s4le()
            self.beatmap_md5_hash = OsuScores.String(self._io, self, self._root)
            self.player_name = OsuScores.String(self._io, self, self._root)
            self.replay_md5_hash = OsuScores.String(self._io, self, self._root)
            self.num_300 = self._io.read_s2le()
            self.num_100 = self._io.read_s2le()
            self.num_50 = self._io.read_s2le()
            self.num_gekis = self._io.read_s2le()
            self.num_katus = self._io.read_s2le()
            self.num_miss = self._io.read_s2le()
            self.replay_score = self._io.read_s4le()
            self.max_combo = self._io.read_s2le()
            self.perfect_combo = OsuScores.Bool(self._io, self, self._root)
            self.mods = self._io.read_s4le()
            self.empty = OsuScores.String(self._io, self, self._root)
            self.replay_timestamp = self._io.read_s8le()
            self.minus_one = self._io.read_bytes(4)
            if not self.minus_one == b"\xFF\xFF\xFF\xFF":
                raise kaitaistruct.ValidationNotEqualError(b"\xFF\xFF\xFF\xFF", self.minus_one, self._io, u"/types/score/seq/17")
            self.online_score_id = self._io.read_s8le()



