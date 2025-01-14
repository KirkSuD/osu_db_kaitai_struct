meta:
  id: osu_scores
  title: scores.db in osu!
  application: osu!
  file-extension: db
  ks-version: 0.7
  imports:
    - vlq_base128_le
  encoding: UTF-8
  endian: le
doc: scores.db file format in rhythm game, osu!.
doc-ref: https://github.com/ppy/osu/wiki/Legacy-database-file-structure
seq:
  - id: version
    type: s4
    doc: Int, Version (e.g. 20150204)
  - id: num_beatmaps
    type: s4
    doc: Int, Number of beatmaps
  - id: beatmaps
    type: beatmap
    repeat: expr
    repeat-expr: num_beatmaps
    doc: Beatmaps*, Aforementioned beatmaps
types:
  bool:
    seq:
      - id: byte
        type: s1
    instances:
      value:
        value: 'byte == 0 ? false : true'
  string:
    seq:
      - id: is_present
        type: s1
      - id: len_str
        type: vlq_base128_le
        if: is_present == 0x0b
      - id: value
        size: len_str.value
        type: str
        if: is_present == 0x0b
  beatmap:
    seq:
      - id: md5_hash
        type: string
        doc: String, Beatmap MD5 hash
      - id: num_scores
        type: s4
        doc: Int, Number of scores on this beatmap
      - id: scores
        type: score
        repeat: expr
        repeat-expr: num_scores
        doc: Score*, Aforementioned scores
  score:
    seq:
      - id: gameplay_mode
        type: s1
        doc: Byte, osu! gameplay mode (0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = Mania)
      - id: version
        type: s4
        doc: Int, Version of this score/replay (e.g. 20150203)
      - id: beatmap_md5_hash
        type: string
        doc: String, Beatmap MD5 hash
      - id: player_name
        type: string
        doc: String, Player name
      - id: replay_md5_hash
        type: string
        doc: String, Replay MD5 hash
      - id: num_300
        type: s2
        doc: Short, Number of 300's
      - id: num_100
        type: s2
        doc: Short, Number of 100's in osu!Standard, 150's in Taiko, 100's in CTB, 100's in Mania
      - id: num_50
        type: s2
        doc: Short, Number of 50's in osu!Standard, small fruit in CTB, 50's in Mania
      - id: num_gekis
        type: s2
        doc: Short, Number of Gekis in osu!Standard, Max 300's in Mania
      - id: num_katus
        type: s2
        doc: Short, Number of Katus in osu!Standard, 200's in Mania
      - id: num_miss
        type: s2
        doc: Short, Number of misses
      - id: replay_score
        type: s4
        doc: Int, Replay score
      - id: max_combo
        type: s2
        doc: Short, Max Combo
      - id: perfect_combo
        type: bool
        doc: Boolean, Perfect combo
      - id: mods
        type: s4
        doc: Int, Bitwise combination of mods used. See Osr (file format) for more information.
      - id: empty
        type: string
        doc: String, Should always be empty
      - id: replay_timestamp
        type: s8
        doc: Long, Timestamp of replay, in Windows ticks
      - id: minus_one
        # type: s4
        contents: [0xff, 0xff, 0xff, 0xff]
        doc: Int, Should always be 0xffffffff (-1).
      - id: online_score_id
        type: s8
        doc: Long, Online Score ID
      # - id: mod_info
      #   type: f8
      #   doc: |
      #     Double, Additional mod information. Only present if Target Practice is enabled.
      #     Mod: Target Practice: Total accuracy of all hits.
      #     Divide this by the number of targets in the map to
      #     find the accuracy displayed in-game.
