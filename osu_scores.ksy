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
doc: |
  scores.db file format in rhythm game osu!,
  the legacy DB file structure used in the old osu stable client (not lazer).

  DB files are in the `osu-stable` installation directory:
  Windows: `%localappdata%\osu!`
  Mac OSX: `/Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/`

  Unless otherwise specified, all numerical types are stored little-endian.
  Integer values, including bytes, are all unsigned.
  UTF-8 characters are stored in their canonical form, with the higher-order byte first.

  scores.db contains the scores achieved locally.
doc-ref: https://github.com/ppy/osu/wiki/Legacy-database-file-structure
seq:
  - id: version
    type: u4
    doc: Int, Version (e.g. 20150204)
  - id: num_beatmaps
    type: u4
    doc: Int, Number of beatmaps
  - id: beatmaps
    type: beatmap
    repeat: expr
    repeat-expr: num_beatmaps
    doc: Beatmaps*, Aforementioned beatmaps
types:
  bool:
    doc: 0x00 for false, everything else is true
    seq:
      - id: byte
        type: u1
    instances:
      value:
        value: 'byte == 0 ? false : true'
  string:
    doc: |
      Has three parts; a single byte which will be either 0x00, indicating that
      the next two parts are not present, or 0x0b (decimal 11), indicating that
      the next two parts are present.
      If it is 0x0b, there will then be a ULEB128, representing the byte length
      of the following string, and then the string itself, encoded in UTF-8.
      See https://en.wikipedia.org/wiki/UTF-8.
    seq:
      - id: is_present
        type: u1
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
        type: u4
        doc: Int, Number of scores on this beatmap
      - id: scores
        type: score
        repeat: expr
        repeat-expr: num_scores
        doc: Score*, Aforementioned scores
  score:
    seq:
      - id: gameplay_mode
        type: u1
        doc: Byte, osu! gameplay mode (0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = Mania)
      - id: version
        type: u4
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
        type: u2
        doc: Short, Number of 300's
      - id: num_100
        type: u2
        doc: Short, Number of 100's in osu!Standard, 150's in Taiko, 100's in CTB, 100's in Mania
      - id: num_50
        type: u2
        doc: Short, Number of 50's in osu!Standard, small fruit in CTB, 50's in Mania
      - id: num_gekis
        type: u2
        doc: Short, Number of Gekis in osu!Standard, Max 300's in Mania
      - id: num_katus
        type: u2
        doc: Short, Number of Katus in osu!Standard, 200's in Mania
      - id: num_miss
        type: u2
        doc: Short, Number of misses
      - id: replay_score
        type: u4
        doc: Int, Replay score
      - id: max_combo
        type: u2
        doc: Short, Max Combo
      - id: perfect_combo
        type: bool
        doc: Boolean, Perfect combo
      - id: mods
        type: u4
        doc: |
          Int, Bitwise combination of mods used.
          See https://osu.ppy.sh/wiki/osu!_File_Formats/Osr_(file_format) for more information.
      - id: empty
        type: string
        doc: String, Should always be empty
      - id: replay_timestamp
        type: u8
        doc: Long, Timestamp of replay, in Windows ticks
      - id: minus_one
        contents: [0xff, 0xff, 0xff, 0xff]
        doc: Int, Should always be 0xffffffff (-1).
      - id: online_score_id
        type: u8
        doc: Long, Online Score ID
      - id: mod_info
        type: f8
        if: (mods & (1 << 23)) != 0
        doc: |
          Double, Additional mod information. Only present if Target Practice is enabled.
          Additional mod information: Target Practice: Total accuracy of all hits.
          Divide this by the number of targets in the map to
          find the accuracy displayed in-game.
