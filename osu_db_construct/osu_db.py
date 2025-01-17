from construct import (
    Struct, LazyBound, Array, Const, Flag, Switch, Default,
    If, Int8ub, Int16ul, Int32ul, Int64ul, Float64l, Float32l, this
)
from osu_string import osu_string
from array_adapter import ArrayAdapter

osu_db__timing_point = Struct(
    'bpm' / Float64l,
    'offset' / Float64l,
    'not_inherited' / Flag,
)

osu_db__beatmap = Struct(
    'len_beatmap' / Default(If(this._root.osu_version < 20191106, Int32ul), 0),
    'artist_name' / LazyBound(lambda: osu_string),
    'artist_name_unicode' / LazyBound(lambda: osu_string),
    'song_title' / LazyBound(lambda: osu_string),
    'song_title_unicode' / LazyBound(lambda: osu_string),
    'creator_name' / LazyBound(lambda: osu_string),
    'difficulty' / LazyBound(lambda: osu_string),
    'audio_file_name' / LazyBound(lambda: osu_string),
    'md5_hash' / LazyBound(lambda: osu_string),
    'osu_file_name' / LazyBound(lambda: osu_string),
    'ranked_status' / Int8ub,
    'num_hitcircles' / Int16ul,
    'num_sliders' / Int16ul,
    'num_spinners' / Int16ul,
    'last_modification_time' / Int64ul,
    'approach_rate' / Switch(this._root.osu_version < 20140609, {True: Int8ub, False: Float32l, }),
    'circle_size' / Switch(this._root.osu_version < 20140609, {True: Int8ub, False: Float32l, }),
    'hp_drain' / Switch(this._root.osu_version < 20140609, {True: Int8ub, False: Float32l, }),
    'overall_difficulty' / Switch(
        this._root.osu_version < 20140609, {True: Int8ub, False: Float32l, }),
    'slider_velocity' / Float64l,
    'star_rating_osu' / If(
        this._root.osu_version >= 20140609,
        Switch(this._root.osu_version <= 20250107, {
            True: LazyBound(lambda: osu_db__int_double_pairs),
            False: LazyBound(lambda: osu_db__int_float_pairs), })),
    'star_rating_taiko' / If(
        this._root.osu_version >= 20140609,
        Switch(this._root.osu_version <= 20250107, {
            True: LazyBound(lambda: osu_db__int_double_pairs),
            False: LazyBound(lambda: osu_db__int_float_pairs), })),
    'star_rating_ctb' / If(
        this._root.osu_version >= 20140609,
        Switch(this._root.osu_version <= 20250107, {
            True: LazyBound(lambda: osu_db__int_double_pairs),
            False: LazyBound(lambda: osu_db__int_float_pairs), })),
    'star_rating_mania' / If(
        this._root.osu_version >= 20140609,
        Switch(this._root.osu_version <= 20250107, {
            True: LazyBound(lambda: osu_db__int_double_pairs),
            False: LazyBound(lambda: osu_db__int_float_pairs), })),
    'drain_time' / Int32ul,
    'total_time' / Int32ul,
    'audio_preview_start_time' / Int32ul,
    'timing_points' / LazyBound(lambda: osu_db__timing_points),
    'difficulty_id' / Int32ul,
    'beatmap_id' / Int32ul,
    'thread_id' / Int32ul,
    'grade_osu' / Int8ub,
    'grade_taiko' / Int8ub,
    'grade_ctb' / Int8ub,
    'grade_mania' / Int8ub,
    'local_beatmap_offset' / Int16ul,
    'stack_leniency' / Float32l,
    'gameplay_mode' / Int8ub,
    'song_source' / LazyBound(lambda: osu_string),
    'song_tags' / LazyBound(lambda: osu_string),
    'online_offset' / Int16ul,
    'song_title_font' / LazyBound(lambda: osu_string),
    'is_unplayed' / Flag,
    'last_played_time' / Int64ul,
    'is_osz2' / Flag,
    'folder_name' / LazyBound(lambda: osu_string),
    'last_check_repo_time' / Int64ul,
    'ignore_sound' / Flag,
    'ignore_skin' / Flag,
    'disable_storyboard' / Flag,
    'disable_video' / Flag,
    'visual_override' / Flag,
    'unknown_short' / Default(If(this._root.osu_version < 20140609, Int16ul), 0),
    'last_modification_time_int' / Int32ul,
    'mania_scroll_speed' / Int8ub,
)

osu_db__timing_points = Struct(
    'num_points' / Int32ul,
    'points' / Array(this.num_points, LazyBound(lambda: osu_db__timing_point)),
)

osu_db__int_double_pair = Struct(
    'magic1' / Const(b"\x08"),
    'mods' / Int32ul,
    'magic2' / Const(b"\x0d"),
    'rating' / Float64l,
)

osu_db__int_double_pairs = Struct(
    'num_pairs' / Int32ul,
    'pairs' / Array(this.num_pairs, LazyBound(lambda: osu_db__int_double_pair)),
)

osu_db__int_float_pair = Struct(
    'magic1' / Const(b"\x08"),
    'mods' / Int32ul,
    'magic2' / Const(b"\x0c"),
    'rating' / Float32l,
)

osu_db__int_float_pairs = Struct(
    'num_pairs' / Int32ul,
    'pairs' / Array(this.num_pairs, LazyBound(lambda: osu_db__int_float_pair)),
)

osu_db = Struct(
    'osu_version' / Int32ul,
    'folder_count' / Int32ul,
    'account_unlocked' / Flag,
    'account_unlock_date' / Int64ul,
    'player_name' / LazyBound(lambda: osu_string),
    'num_beatmaps' / Int32ul,
    'beatmaps' / Array(this.num_beatmaps, LazyBound(lambda: osu_db__beatmap)),
    'user_permissions' / Int32ul,
)

osu_db__timing_points = ArrayAdapter(
    osu_db__timing_points, {"points": "num_points"}, only_one_field=True)
osu_db__int_double_pairs = ArrayAdapter(
    osu_db__int_double_pairs, {"pairs": "num_pairs"}, only_one_field=True)
osu_db__int_float_pairs = ArrayAdapter(
    osu_db__int_float_pairs, {"pairs": "num_pairs"}, only_one_field=True)
osu_db = ArrayAdapter(osu_db, {"beatmaps": "num_beatmaps"})

if __name__ == "__main__":
    import unittest
    from path_util import get_osu_dir

    file_path = get_osu_dir() / "osu!.db"
    with open(file_path, "rb") as file:
        data = file.read()

    class OsuTestCase(unittest.TestCase):
        def test_round_trip(self):
            parsed = osu_db.parse(data)
            built = osu_db.build(parsed)
            self.assertEqual(data, built)

        def test_build_dummy(self):
            test_data = dict(
                osu_version=20250108,
                folder_count=100,
                account_unlocked=True,
                account_unlock_date=0,
                player_name="player",
                beatmaps=[dict(
                    artist_name="artist",
                    artist_name_unicode="artist ♪",
                    song_title="song",
                    song_title_unicode="song ♪",
                    creator_name="creator",
                    difficulty="Expert",
                    audio_file_name="audio.mp3",
                    md5_hash="deadbeef",
                    osu_file_name="song [Expert].osu",
                    ranked_status=4,
                    num_hitcircles=100,
                    num_sliders=100,
                    num_spinners=100,
                    last_modification_time=1000000,
                    approach_rate=9.2,
                    circle_size=4.2,
                    hp_drain=7.2,
                    overall_difficulty=8.2,
                    slider_velocity=2.4,
                    star_rating_osu=[dict(mods=0, rating=5.3)],
                    star_rating_taiko=[],
                    star_rating_ctb=[],
                    star_rating_mania=[],
                    drain_time=75,
                    total_time=80000,
                    audio_preview_start_time=50000,
                    timing_points=[dict(bpm=600, offset=5000, not_inherited=True)],
                    difficulty_id=1200000,
                    beatmap_id=600000,
                    thread_id=0,
                    grade_osu=9,
                    grade_taiko=9,
                    grade_ctb=9,
                    grade_mania=9,
                    local_beatmap_offset=0,
                    stack_leniency=0.2,
                    gameplay_mode=0,
                    song_source="source",
                    song_tags="TagA TagB",
                    online_offset=0,
                    song_title_font="",
                    is_unplayed=True,
                    last_played_time=0,
                    is_osz2=False,
                    folder_name="600000 artist - song",
                    last_check_repo_time=1000000,
                    ignore_sound=False,
                    ignore_skin=False,
                    disable_storyboard=False,
                    disable_video=False,
                    visual_override=False,
                    last_modification_time_int=0,
                    mania_scroll_speed=0,
                )],
                user_permissions=1
            )
            built = osu_db.build(test_data)
            parsed = osu_db.parse(built)
            built_again = osu_db.build(parsed)
            self.assertEqual(built, built_again)

    unittest.main()
