meta:
  id: osu_db
  title: osu!.db in osu!
  application: osu!
  file-extension: db
  ks-version: 0.7
  imports:
    - vlq_base128_le
  encoding: UTF-8
  endian: le
doc: osu!.db file format in rhythm game, osu!.
doc-ref: https://osu.ppy.sh/wiki/zh-tw/osu%21_File_Formats/Db_%28file_format%29
seq:
  - id: osu_version
    type: s4
    doc: Int, osu! version (e.g. 20150203)
  - id: folder_count
    type: s4
    doc: Int, Folder Count
  - id: account_unlocked
    type: bool
    doc: Bool, AccountUnlocked (only false when the account is locked or banned in any way)
  - id: account_unlock_date
    type: s8
    doc: DateTime, Date the account will be unlocked
  - id: player_name
    type: string
    doc: String, Player name
  - id: num_beatmaps
    type: s4
    doc: Int, Number of beatmaps
  - id: beatmaps
    type: beatmap
    repeat: expr
    repeat-expr: num_beatmaps
    doc: Beatmaps*, Aforementioned beatmaps
  - id: user_permissions
    type: s4
    doc: Int, User permissions (0 = None, 1 = Normal, 2 = Moderator, 4 = Supporter, 8 = Friend, 16 = peppy, 32 = World Cup staff)
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
  int_double_pair:
    doc: |
      The first byte is 0x08, followed by an Int, then 0x0d, followed by a Double.
      These extraneous bytes are presumably flags to signify different data types
      in these slots, though in practice no other such flags have been seen.
      Currently the purpose of this data type is unknown.
    seq:
      - id: magic1
        contents: [0x08]
      - id: int
        type: s4
      - id: magic2
        contents: [0x0d]
      - id: double
        type: f8
  int_double_pairs:
    doc: An Int indicating the number of following Int-Double pairs, then the aforementioned pairs.
    seq:
      - id: num_pairs
        type: s4
      - id: pairs
        type: int_double_pair
        repeat: expr
        repeat-expr: num_pairs
  timing_point:
    doc: |
      Consists of a Double, signifying the BPM, another Double,
      signifying the offset into the song, in milliseconds, and a Boolean;
      if false, then this timing point is inherited.
      See Osu (file format) for more information regarding timing points.
    seq:
      - id: bpm
        type: f8
      - id: offset
        type: f8
      - id: not_inherited
        type: bool
  timing_points:
    doc: An Int indicating the number of following Timing points, then the aforementioned Timing points.
    seq:
      - id: num_points
        type: s4
      - id: points
        type: timing_point
        repeat: expr
        repeat-expr: num_points
  beatmap:
    seq:
      - id: len_beatmap
        type: s4
        if: _root.osu_version < 20191106
        doc: Int,	Size in bytes of the beatmap entry. Only present if version is less than 20191106.
      - id: artist_name
        type: string
        doc: String, Artist name
      - id: artist_name_unicode
        type: string
        doc: String, Artist name, in Unicode
      - id: song_title
        type: string
        doc: String, Song title
      - id: song_title_unicode
        type: string
        doc: String, Song title, in Unicode
      - id: creator_name
        type: string
        doc: String, Creator name
      - id: difficulty
        type: string
        doc: String, Difficulty (e.g. Hard, Insane, etc.)
      - id: audio_file_name
        type: string
        doc: String, Audio file name
      - id: md5_hash
        type: string
        doc: String, MD5 hash of the beatmap
      - id: osu_file_name
        type: string
        doc: String, Name of the .osu file corresponding to this beatmap
      - id: ranked_status
        type: s1
        doc: Byte, Ranked status (0 = unknown, 1 = unsubmitted, 2 = pending/wip/graveyard, 3 = unused, 4 = ranked, 5 = approved, 6 = qualified, 7 = loved)
      - id: num_hitcircles
        type: s2
        doc: Short, Number of hitcircles
      - id: num_sliders
        type: s2
        doc: 'Short, Number of sliders (note: this will be present in every mode)'
      - id: num_spinners
        type: s2
        doc: 'Short, Number of spinners (note: this will be present in every mode)'
      - id: last_modification_time
        type: s8
        doc: Long, Last modification time, Windows ticks.
      - id: approach_rate_byte
        type: s1
        if: _root.osu_version < 20140609
        doc: Byte/Single, Approach rate. Byte if the version is less than 20140609, Single otherwise.
      - id: approach_rate
        type: f4
        if: _root.osu_version >= 20140609
        doc: Byte/Single, Approach rate. Byte if the version is less than 20140609, Single otherwise.
      - id: circle_size_byte
        type: s1
        if: _root.osu_version < 20140609
        doc: Byte/Single, Circle size. Byte if the version is less than 20140609, Single otherwise.
      - id: circle_size
        type: f4
        if: _root.osu_version >= 20140609
        doc: Byte/Single, Circle size. Byte if the version is less than 20140609, Single otherwise.
      - id: hp_drain_byte
        type: s1
        if: _root.osu_version < 20140609
        doc: Byte/Single, HP drain. Byte if the version is less than 20140609, Single otherwise.
      - id: hp_drain
        type: f4
        if: _root.osu_version >= 20140609
        doc: Byte/Single, HP drain. Byte if the version is less than 20140609, Single otherwise.
      - id: overall_difficulty_byte
        type: s1
        if: _root.osu_version < 20140609
        doc: Byte/Single, Overall difficulty. Byte if the version is less than 20140609, Single otherwise.
      - id: overall_difficulty
        type: f4
        if: _root.osu_version >= 20140609
        doc: Byte/Single, Overall difficulty. Byte if the version is less than 20140609, Single otherwise.
      - id: slider_velocity
        type: f8
        doc: Double, Slider velocity
      - id: star_rating_osu
        type: int_double_pairs
        if: _root.osu_version >= 20140609
        doc: Int-Double pair*, Star Rating info for osu! standard, in each pair, the Int is the mod combination, and the Double is the Star Rating. Only present if version is greater than or equal to 20140609.
      - id: star_rating_taiko
        type: int_double_pairs
        if: _root.osu_version >= 20140609
        doc: Int-Double pair*, Star Rating info for Taiko, in each pair, the Int is the mod combination, and the Double is the Star Rating. Only present if version is greater than or equal to 20140609.
      - id: star_rating_ctb
        type: int_double_pairs
        if: _root.osu_version >= 20140609
        doc: Int-Double pair*, Star Rating info for CTB, in each pair, the Int is the mod combination, and the Double is the Star Rating. Only present if version is greater than or equal to 20140609.
      - id: star_rating_mania
        type: int_double_pairs
        if: _root.osu_version >= 20140609
        doc: Int-Double pair*, Star Rating info for osu!mania, in each pair, the Int is the mod combination, and the Double is the Star Rating. Only present if version is greater than or equal to 20140609.
      - id: drain_time
        type: s4
        doc: Int, Drain time, in seconds
      - id: total_time
        type: s4
        doc: Int, Total time, in milliseconds
      - id: audio_preview_start_time
        type: s4
        doc: Int, Time when the audio preview when hovering over a beatmap in beatmap select starts, in milliseconds.
      - id: timing_points
        type: timing_points
        doc: Timing point+, An Int indicating the number of following Timing points, then the aforementioned Timing points.
      - id: beatmap_id
        type: s4
        doc: Int, Beatmap ID
      - id: beatmap_set_id
        type: s4
        doc: Int, Beatmap set ID
      - id: thread_id
        type: s4
        doc: Int, Thread ID
      - id: grade_osu
        type: s1
        doc: Byte, Grade achieved in osu! standard.
      - id: grade_taiko
        type: s1
        doc: Byte, Grade achieved in Taiko.
      - id: grade_ctb
        type: s1
        doc: Byte, Grade achieved in CTB.
      - id: grade_mania
        type: s1
        doc: Byte, Grade achieved in osu!mania.
      - id: local_beatmap_offset
        type: s2
        doc: Short, Local beatmap offset
      - id: stack_leniency
        type: f4
        doc: Single, Stack leniency
      - id: gameplay_mode
        type: s1
        doc: Byte, Osu gameplay mode. 0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = Mania
      - id: song_source
        type: string
        doc: String, Song source
      - id: song_tags
        type: string
        doc: String, Song tags
      - id: online_offset
        type: s2
        doc: Short, Online offset
      - id: song_title_font
        type: string
        doc: String, Font used for the title of the song
      - id: is_unplayed
        type: bool
        doc: Boolean, Is beatmap unplayed
      - id: last_played_time
        type: s8
        doc: Long, Last time when beatmap was played
      - id: is_osz2
        type: bool
        doc: Boolean, Is the beatmap osz2
      - id: folder_name
        type: string
        doc: String, Folder name of the beatmap, relative to Songs folder
      - id: last_check_repo_time
        type: s8
        doc: Long, Last time when beatmap was checked against osu! repository
      - id: ignore_sound
        type: bool
        doc: Boolean, Ignore beatmap sound
      - id: ignore_skin
        type: bool
        doc: Boolean, Ignore beatmap skin
      - id: disable_storyboard
        type: bool
        doc: Boolean, Disable storyboard
      - id: disable_video
        type: bool
        doc: Boolean, Disable video
      - id: visual_override
        type: bool
        doc: Boolean, Visual override
      - id: unknown_short
        type: s2
        if: _root.osu_version < 20140609
        doc: Short?, Unknown. Only present if version is less than 20140609.
      - id: last_modification_time_int
        type: s4
        doc: Int, Last modification time (?)
      - id: mania_scroll_speed
        type: s1
        doc: Byte, Mania scroll speed
