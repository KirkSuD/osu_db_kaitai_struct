from construct import (
    Struct, LazyBound, Array, Const, Flag, Default,
    If, Int8ub, Int16ul, Int32ul, Int64ul, Float64l, this
)
from osu_string import osu_string
from array_adapter import ArrayAdapter

osu_scores__beatmap = Struct(
    'md5_hash' / LazyBound(lambda: osu_string),
    'num_scores' / Int32ul,
    'scores' / Array(this.num_scores, LazyBound(lambda: osu_scores__score)),
)

osu_scores__score = Struct(
    'gameplay_mode' / Int8ub,
    'version' / Int32ul,
    'beatmap_md5_hash' / LazyBound(lambda: osu_string),
    'player_name' / LazyBound(lambda: osu_string),
    'replay_md5_hash' / LazyBound(lambda: osu_string),
    'num_300' / Int16ul,
    'num_100' / Int16ul,
    'num_50' / Int16ul,
    'num_gekis' / Int16ul,
    'num_katus' / Int16ul,
    'num_miss' / Int16ul,
    'replay_score' / Int32ul,
    'max_combo' / Int16ul,
    'perfect_combo' / Flag,
    'mods' / Int32ul,
    'empty' / Default(LazyBound(lambda: osu_string), None),
    'replay_timestamp' / Int64ul,
    'minus_one' / Const(b"\xff\xff\xff\xff"),
    'online_score_id' / Int64ul,
    'mod_info' / Default(If((this.mods & (1 << 23)) != 0, Float64l), 0)
)

osu_scores = Struct(
    'version' / Int32ul,
    'num_beatmaps' / Int32ul,
    'beatmaps' / Array(this.num_beatmaps, LazyBound(lambda: osu_scores__beatmap)),
)

osu_scores__beatmap = ArrayAdapter(osu_scores__beatmap, {"scores": "num_scores"})
osu_scores = ArrayAdapter(osu_scores, {"beatmaps": "num_beatmaps"})

if __name__ == "__main__":
    import unittest
    from path_util import get_osu_dir

    file_path = get_osu_dir() / "scores.db"
    with open(file_path, "rb") as file:
        data = file.read()

    class ScoresTestCase(unittest.TestCase):
        def test_round_trip(self):
            parsed = osu_scores.parse(data)
            built = osu_scores.build(parsed)
            self.assertEqual(data, built)

        def test_build_dummy(self):
            test_data = dict(
                version=20250108,
                beatmaps=[dict(
                    md5_hash="deadbeef",
                    scores=[dict(
                        gameplay_mode=0,
                        version=20250108,
                        beatmap_md5_hash="deadbeef",
                        player_name="player",
                        replay_md5_hash="deadbeef",
                        num_300=10,
                        num_100=10,
                        num_50=10,
                        num_gekis=10,
                        num_katus=10,
                        num_miss=10,
                        replay_score=1000,
                        max_combo=10,
                        perfect_combo=False,
                        mods=0,
                        replay_timestamp=1000000,
                        online_score_id=0,
                        # mod_info=0,  # Traget Practice mod
                    )]
                )]
            )
            built = osu_scores.build(test_data)
            parsed = osu_scores.parse(built)
            built_again = osu_scores.build(parsed)
            self.assertEqual(built, built_again)

    unittest.main()
