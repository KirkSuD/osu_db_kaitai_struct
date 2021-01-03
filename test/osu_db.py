# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import vlq_base128_le
class OsuDb(KaitaiStruct):
    """osu!.db file format in rhythm game, osu!.
    
    .. seealso::
       Source - https://osu.ppy.sh/wiki/zh-tw/osu%21_File_Formats/Db_%28file_format%29
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.osu_version = self._io.read_s4le()
        self.folder_count = self._io.read_s4le()
        self.account_unlocked = OsuDb.Bool(self._io, self, self._root)
        self.account_unlock_date = self._io.read_s8le()
        self.player_name = OsuDb.String(self._io, self, self._root)
        self.num_beatmaps = self._io.read_s4le()
        self.beatmaps = [None] * (self.num_beatmaps)
        for i in range(self.num_beatmaps):
            self.beatmaps[i] = OsuDb.Beatmap(self._io, self, self._root)

        self.user_permissions = self._io.read_s4le()

    class TimingPoint(KaitaiStruct):
        """Consists of a Double, signifying the BPM, another Double,
        signifying the offset into the song, in milliseconds, and a Boolean;
        if false, then this timing point is inherited.
        See Osu (file format) for more information regarding timing points.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bpm = self._io.read_f8le()
            self.offset = self._io.read_f8le()
            self.not_inherited = OsuDb.Bool(self._io, self, self._root)


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
            if self._root.osu_version < 20191106:
                self.len_beatmap = self._io.read_s4le()

            self.artist_name = OsuDb.String(self._io, self, self._root)
            self.artist_name_unicode = OsuDb.String(self._io, self, self._root)
            self.song_title = OsuDb.String(self._io, self, self._root)
            self.song_title_unicode = OsuDb.String(self._io, self, self._root)
            self.creator_name = OsuDb.String(self._io, self, self._root)
            self.difficulty = OsuDb.String(self._io, self, self._root)
            self.audio_file_name = OsuDb.String(self._io, self, self._root)
            self.md5_hash = OsuDb.String(self._io, self, self._root)
            self.osu_file_name = OsuDb.String(self._io, self, self._root)
            self.ranked_status = self._io.read_s1()
            self.num_hitcircles = self._io.read_s2le()
            self.num_sliders = self._io.read_s2le()
            self.num_spinners = self._io.read_s2le()
            self.last_modification_time = self._io.read_s8le()
            if self._root.osu_version < 20140609:
                self.approach_rate_byte = self._io.read_s1()

            if self._root.osu_version >= 20140609:
                self.approach_rate = self._io.read_f4le()

            if self._root.osu_version < 20140609:
                self.circle_size_byte = self._io.read_s1()

            if self._root.osu_version >= 20140609:
                self.circle_size = self._io.read_f4le()

            if self._root.osu_version < 20140609:
                self.hp_drain_byte = self._io.read_s1()

            if self._root.osu_version >= 20140609:
                self.hp_drain = self._io.read_f4le()

            if self._root.osu_version < 20140609:
                self.overall_difficulty_byte = self._io.read_s1()

            if self._root.osu_version >= 20140609:
                self.overall_difficulty = self._io.read_f4le()

            self.slider_velocity = self._io.read_f8le()
            if self._root.osu_version >= 20140609:
                self.star_rating_osu = OsuDb.IntDoublePairs(self._io, self, self._root)

            if self._root.osu_version >= 20140609:
                self.star_rating_taiko = OsuDb.IntDoublePairs(self._io, self, self._root)

            if self._root.osu_version >= 20140609:
                self.star_rating_ctb = OsuDb.IntDoublePairs(self._io, self, self._root)

            if self._root.osu_version >= 20140609:
                self.star_rating_mania = OsuDb.IntDoublePairs(self._io, self, self._root)

            self.drain_time = self._io.read_s4le()
            self.total_time = self._io.read_s4le()
            self.audio_preview_start_time = self._io.read_s4le()
            self.timing_points = OsuDb.TimingPoints(self._io, self, self._root)
            self.beatmap_id = self._io.read_s4le()
            self.beatmap_set_id = self._io.read_s4le()
            self.thread_id = self._io.read_s4le()
            self.grade_osu = self._io.read_s1()
            self.grade_taiko = self._io.read_s1()
            self.grade_ctb = self._io.read_s1()
            self.grade_mania = self._io.read_s1()
            self.local_beatmap_offset = self._io.read_s2le()
            self.stack_leniency = self._io.read_f4le()
            self.gameplay_mode = self._io.read_s1()
            self.song_source = OsuDb.String(self._io, self, self._root)
            self.song_tags = OsuDb.String(self._io, self, self._root)
            self.online_offset = self._io.read_s2le()
            self.song_title_font = OsuDb.String(self._io, self, self._root)
            self.is_unplayed = OsuDb.Bool(self._io, self, self._root)
            self.last_played_time = self._io.read_s8le()
            self.is_osz2 = OsuDb.Bool(self._io, self, self._root)
            self.folder_name = OsuDb.String(self._io, self, self._root)
            self.last_check_repo_time = self._io.read_s8le()
            self.ignore_sound = OsuDb.Bool(self._io, self, self._root)
            self.ignore_skin = OsuDb.Bool(self._io, self, self._root)
            self.disable_storyboard = OsuDb.Bool(self._io, self, self._root)
            self.disable_video = OsuDb.Bool(self._io, self, self._root)
            self.visual_override = OsuDb.Bool(self._io, self, self._root)
            if self._root.osu_version < 20140609:
                self.unknown_short = self._io.read_s2le()

            self.last_modification_time_int = self._io.read_s4le()
            self.mania_scroll_speed = self._io.read_s1()


    class TimingPoints(KaitaiStruct):
        """An Int indicating the number of following Timing points, then the aforementioned Timing points."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_points = self._io.read_s4le()
            self.points = [None] * (self.num_points)
            for i in range(self.num_points):
                self.points[i] = OsuDb.TimingPoint(self._io, self, self._root)



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


    class IntDoublePair(KaitaiStruct):
        """The first byte is 0x08, followed by an Int, then 0x0d, followed by a Double.
        These extraneous bytes are presumably flags to signify different data types
        in these slots, though in practice no other such flags have been seen.
        Currently the purpose of this data type is unknown.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic1 = self._io.read_bytes(1)
            if not self.magic1 == b"\x08":
                raise kaitaistruct.ValidationNotEqualError(b"\x08", self.magic1, self._io, u"/types/int_double_pair/seq/0")
            self.int = self._io.read_s4le()
            self.magic2 = self._io.read_bytes(1)
            if not self.magic2 == b"\x0D":
                raise kaitaistruct.ValidationNotEqualError(b"\x0D", self.magic2, self._io, u"/types/int_double_pair/seq/2")
            self.double = self._io.read_f8le()


    class IntDoublePairs(KaitaiStruct):
        """An Int indicating the number of following Int-Double pairs, then the aforementioned pairs."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_pairs = self._io.read_s4le()
            self.pairs = [None] * (self.num_pairs)
            for i in range(self.num_pairs):
                self.pairs[i] = OsuDb.IntDoublePair(self._io, self, self._root)




