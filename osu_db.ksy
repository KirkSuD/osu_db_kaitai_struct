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
doc: |
  osu!.db file format in rhythm game osu!,
  the legacy DB file structure used in the old osu stable client (not lazer).

  DB files are in the `osu-stable` installation directory:
  Windows: `%localappdata%\osu!`
  Mac OSX: `/Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/`

  Unless otherwise specified, all numerical types are stored little-endian.
  Integer values, including bytes, are all unsigned.
  UTF-8 characters are stored in their canonical form, with the higher-order byte first.

  osu!.db contains a cached version of information about all currently installed beatmaps.
  Deleting this file will force osu! to rebuild the cache from scratch.
  This may be useful since it may fix certain discrepancies, such as beatmaps
  that had been deleted from the Songs folder but are still showing up in-game.
  Unsurprisingly, due to its central role in the internal management of beatmaps
  and the amount of data that is cached, osu!.db is the largest of the .db files.
doc-ref: https://github.com/ppy/osu/wiki/Legacy-database-file-structure
seq:
  - id: osu_version
    type: u4
    doc: Int, osu! version (e.g. 20150203)
  - id: folder_count
    type: u4
    doc: Int, Folder Count
  - id: account_unlocked
    type: bool
    doc: Bool, AccountUnlocked (only false when the account is locked or banned in any way)
  - id: account_unlock_date
    type: u8
    doc: |
      DateTime, Date the account will be unlocked.
      A 64-bit number of ticks representing a date and time.
      Ticks are the amount of 100-nanosecond intervals since midnight, January 1, 0001 UTC.
      See https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=netframework-4.7.2
      for more information.
  - id: player_name
    type: string
    doc: String, Player name
  - id: num_beatmaps
    type: u4
    doc: Int, Number of beatmaps
  - id: beatmaps
    type: beatmap
    repeat: expr
    repeat-expr: num_beatmaps
    doc: Beatmaps*, Aforementioned beatmaps
  - id: user_permissions
    type: u4
    doc: |
      Int, User permissions (
      0 = None, 1 = Normal, 2 = Moderator, 4 = Supporter,
      8 = Friend, 16 = peppy, 32 = World Cup staff)
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
  int_float_pair:
    doc: |
      The first byte is 0x08, followed by an Int, then 0x0c, followed by a Float.
    seq:
      - id: magic1
        contents: [0x08]
      - id: int
        type: u4
      - id: magic2
        contents: [0x0c]
      - id: float
        type: f4
  int_float_pairs:
    doc: An Int indicating the number of following Int-Float pairs, then the aforementioned pairs.
    seq:
      - id: num_pairs
        type: u4
      - id: pairs
        type: int_float_pair
        repeat: expr
        repeat-expr: num_pairs
  int_double_pair:
    doc: |
      The first byte is 0x08, followed by an Int, then 0x0d, followed by a Double.
    seq:
      - id: magic1
        contents: [0x08]
      - id: int
        type: u4
      - id: magic2
        contents: [0x0d]
      - id: double
        type: f8
  int_double_pairs:
    doc: An Int indicating the number of following Int-Double pairs, then the aforementioned pairs.
    seq:
      - id: num_pairs
        type: u4
      - id: pairs
        type: int_double_pair
        repeat: expr
        repeat-expr: num_pairs
  timing_point:
    doc: |
      Consists of a Double, signifying the BPM, another Double,
      signifying the offset into the song, in milliseconds, and a Boolean;
      if false, then this timing point is inherited.
      See https://osu.ppy.sh/wiki/osu!_File_Formats/Osu_(file_format)
      for more information regarding timing points.
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
        type: u4
      - id: points
        type: timing_point
        repeat: expr
        repeat-expr: num_points
  beatmap:
    seq:
      - id: len_beatmap
        type: u4
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
        type: u1
        doc: |
          Byte, Ranked status (
          0 = unknown, 1 = unsubmitted, 2 = pending/wip/graveyard,
          3 = unused, 4 = ranked, 5 = approved, 6 = qualified, 7 = loved)
      - id: num_hitcircles
        type: u2
        doc: Short, Number of hitcircles
      - id: num_sliders
        type: u2
        doc: 'Short, Number of sliders (note: this will be present in every mode)'
      - id: num_spinners
        type: u2
        doc: 'Short, Number of spinners (note: this will be present in every mode)'
      - id: last_modification_time
        type: u8
        doc: Long, Last modification time, Windows ticks.
      - id: approach_rate
        type:
          switch-on: _root.osu_version < 20140609
          cases:
            true: u1
            false: f4
        doc: Byte/Single, Approach rate. Byte if the version is less than 20140609, Single otherwise.
      - id: circle_size
        type: 
          switch-on: _root.osu_version < 20140609
          cases:
            true: u1
            false: f4
        doc: Byte/Single, Circle size. Byte if the version is less than 20140609, Single otherwise.
      - id: hp_drain
        type: 
          switch-on: _root.osu_version < 20140609
          cases:
            true: u1
            false: f4
        doc: Byte/Single, HP drain. Byte if the version is less than 20140609, Single otherwise.
      - id: overall_difficulty
        type:
          switch-on: _root.osu_version < 20140609
          cases:
            true: u1
            false: f4
        doc: Byte/Single, Overall difficulty. Byte if the version is less than 20140609, Single otherwise.
      - id: slider_velocity
        type: f8
        doc: Double, Slider velocity
      - id: star_rating_osu
        type: 
          switch-on: _root.osu_version <= 20250107
          cases:
            true: int_double_pairs
            false: int_float_pairs
        if: _root.osu_version >= 20140609
        doc: |
          Int-Float pair*, Star Rating info for osu! standard, in each pair,
          the Int is the mod combination, and the Float is the Star Rating.
          Only present if version is greater than or equal to 20140609.
          Until database version 20250107, this was a collection of Int-Double pairs.
      - id: star_rating_taiko
        type: 
          switch-on: _root.osu_version <= 20250107
          cases:
            true: int_double_pairs
            false: int_float_pairs
        if: _root.osu_version >= 20140609
        doc: |
          Int-Float pair*, Star Rating info for Taiko, in each pair,
          the Int is the mod combination, and the Float is the Star Rating.
          Only present if version is greater than or equal to 20140609.
          Until database version 20250107, this was a collection of Int-Double pairs.
      - id: star_rating_ctb
        type: 
          switch-on: _root.osu_version <= 20250107
          cases:
            true: int_double_pairs
            false: int_float_pairs
        doc: |
          Int-Float pair*, Star Rating info for CTB, in each pair,
          the Int is the mod combination, and the Float is the Star Rating.
          Only present if version is greater than or equal to 20140609.
          Until database version 20250107, this was a collection of Int-Double pairs.
      - id: star_rating_mania
        type: 
          switch-on: _root.osu_version <= 20250107
          cases:
            true: int_double_pairs
            false: int_float_pairs
        if: _root.osu_version >= 20140609
        doc: |
          Int-Float pair*, Star Rating info for osu!mania, in each pair,
          the Int is the mod combination, and the Float is the Star Rating.
          Only present if version is greater than or equal to 20140609.
          Until database version 20250107, this was a collection of Int-Double pairs.
      - id: drain_time
        type: u4
        doc: Int, Drain time, in seconds
      - id: total_time
        type: u4
        doc: Int, Total time, in milliseconds
      - id: audio_preview_start_time
        type: u4
        doc: |
          Int, Time when the audio preview when hovering over a beatmap in beatmap select starts,
          in milliseconds.
      - id: timing_points
        type: timing_points
        doc: |
          Timing point+, An Int indicating the number of following Timing points,
          then the aforementioned Timing points.
      - id: difficulty_id
        type: u4
        doc: Int, Difficulty ID
      - id: beatmap_id
        type: u4
        doc: Int, Beatmap ID
      - id: thread_id
        type: u4
        doc: Int, Thread ID
      - id: grade_osu
        type: u1
        doc: Byte, Grade achieved in osu! standard.
      - id: grade_taiko
        type: u1
        doc: Byte, Grade achieved in Taiko.
      - id: grade_ctb
        type: u1
        doc: Byte, Grade achieved in CTB.
      - id: grade_mania
        type: u1
        doc: Byte, Grade achieved in osu!mania.
      - id: local_beatmap_offset
        type: u2
        doc: Short, Local beatmap offset
      - id: stack_leniency
        type: f4
        doc: Single, Stack leniency
      - id: gameplay_mode
        type: u1
        doc: Byte, Osu gameplay mode. 0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = Mania
      - id: song_source
        type: string
        doc: String, Song source
      - id: song_tags
        type: string
        doc: String, Song tags
      - id: online_offset
        type: u2
        doc: Short, Online offset
      - id: song_title_font
        type: string
        doc: String, Font used for the title of the song
      - id: is_unplayed
        type: bool
        doc: Boolean, Is beatmap unplayed
      - id: last_played_time
        type: u8
        doc: Long, Last time when beatmap was played
      - id: is_osz2
        type: bool
        doc: Boolean, Is the beatmap osz2
      - id: folder_name
        type: string
        doc: String, Folder name of the beatmap, relative to Songs folder
      - id: last_check_repo_time
        type: u8
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
        type: u2
        if: _root.osu_version < 20140609
        doc: Short?, Unknown. Only present if version is less than 20140609.
      - id: last_modification_time_int
        type: u4
        doc: Int, Last modification time (?)
      - id: mania_scroll_speed
        type: u1
        doc: Byte, Mania scroll speed
