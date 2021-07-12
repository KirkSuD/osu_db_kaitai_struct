"""
OsuMusicPlayer - A music player for osu!, parse osu!.db, collection.db,
 then make json to form a static web music player.
Use the Kaitai Struct osu db parser.

Version 0.0
Roughly tested @ 2021/05/04
with osu!.db ver.20210423, collection.db ver.20210423.

osu! directory path:
Windows: %localappdata%/osu!
Mac OSX: /Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/
"""


from osu_db import OsuDb
from osu_collection import OsuCollection


def list_folders(path):
    for _, folders, _ in os.walk(path):
        return folders


def get_song_from_beatmap(beatmap):
    return {
        "artist": beatmap.artist_name.value,
        "title": beatmap.song_title.value,
        "file": beatmap.audio_file_name.value,
        "folder": beatmap.folder_name.value,
        "time": beatmap.total_time
    }


def get_songs(beatmaps):
    """
    Generate a list of songs without duplication.
    """
    folders = set()
    res = []
    for bm in beatmaps:
        if bm.folder_name.value in folders:
            continue
        folders.add(bm.folder_name.value)
        res.append(get_song_from_beatmap(bm))
    return res


def get_md5_to_song_dict(beatmaps):
    """
    Generate a dict from md5 to song with duplications.
    Used by md5_to_song_dict of get_songs_from_md5().
    """
    res = {}
    for bm in beatmaps:
        if bm.md5_hash.value in res:
            raise ValueError("get_md5_to_song_dict(beatmaps): md5 collision: " + bm.md5_hash)
        res[bm.md5_hash.value] = get_song_from_beatmap(bm)
    return res


def get_songs_from_md5(md5_to_song_dict, md5_list):
    """
    Generate a list of songs from a given md5_list by using md5_to_song_dict.
    """
    folder_set = set()
    res = []
    for md5 in md5_list:
        song = md5_to_song_dict[md5.value]
        if song["folder"] in folder_set:
            continue
        folder_set.add(song["folder"])
        res.append(song)
    return res


def get_collections(beatmaps, collections):
    """
    Convert collections md5 to song.
    """
    md5_to_songs = get_md5_to_song_dict(beatmaps)
    return [
        [col.name.value, get_songs_from_md5(md5_to_songs, col.beatmaps_md5s)]
        for col in collections]


def get_current_time():
    return datetime.datetime.now()


def get_time_str(t=None):
    if t is None:
        t = get_current_time()
    return t.strftime("%Y/%m/%d-%H:%M:%S")


class PLSWriter:
    def __init__(self, *args, pretty_blank=False, **kwargs):
        self.file = open(*args, **kwargs)
        self.pretty_blank = pretty_blank
        self.num_entries = 0

    def write(self, file, title=None, length=None):
        if self.num_entries == 0:
            self.file.write("[playlist]\n")
            self._write_blank()

        self.num_entries += 1
        self.file.write("File%d=%s\n" % (self.num_entries, file))
        if title is not None:
            self.file.write("Title%d=%s\n" % (self.num_entries, title))
        if length is not None:
            self.file.write("Length%d=%s\n" % (self.num_entries, length))
        self._write_blank()

    def _write_blank(self):
        if self.pretty_blank:
            self.file.write("\n")

    def close(self):
        self.file.write("NumberOfEntries=%d\n" % self.num_entries)
        self.file.write("Version=2\n")
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class M3UWriter:
    def __init__(self, *args, pretty_blank=False, **kwargs):
        self.file = open(*args, **kwargs)
        self.pretty_blank = pretty_blank
        self.file.write("#EXTM3U\n")
        self._write_blank()

    def write(self, file, title=None, length=None):
        if title is not None or length is not None:
            self.file.write("#EXTINF:")
            if length is not None:
                self.file.write("%s," % length)
            if title is not None:
                self.file.write("%s" % title)

        self.file.write("\n%s\n" % file)
        self._write_blank()

    def _write_blank(self):
        if self.pretty_blank:
            self.file.write("\n")

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == "__main__":
    osu_root_path = r"%localappdata%/osu!"
    copy_db_path = r"./user_data/copied_osu_db"
    osudb_js_path = r"./user_data/osudb.js"
    pls_path = r"./user_data/osu_music.pls"  # the common .pls playlist format
    m3u_path = r"./user_data/osu_music.m3u8"  # the M3U playlist format

    # the osu collection to be converted to playlist, None/False/""/0 to skip
    playlist_collection_name = r"FavoriteMusic"
    playlist_shuffle = False

    import os, shutil, json, datetime, random

    pjoin = os.path.join  # shortcut

    # expandvars: https://stackoverflow.com/questions/53112401/percent-signs-in-windows-path
    # abspath + realpath: https://stackoverflow.com/questions/37863476/
    osu_root_path = os.path.expandvars(osu_root_path)
    copy_db_path = os.path.abspath(os.path.realpath(copy_db_path))
    osudb_js_path = os.path.abspath(os.path.realpath(osudb_js_path))
    pls_path = os.path.abspath(os.path.realpath(pls_path))
    m3u_path = os.path.abspath(os.path.realpath(m3u_path))
    osu_songs_path = pjoin(osu_root_path, "Songs")

    print("osu! root path:", osu_root_path)
    print("osu! songs path:", osu_songs_path)
    print("Copy databases to:", copy_db_path)
    print("osudb.js path:", osudb_js_path)
    print("osu_music.pls path:", pls_path)
    print("osu_music.m3u path:", m3u_path)
    input("Press ENTER to continue...")

    print()
    print("Copying osu!.db and collection.db...")
    os.makedirs(copy_db_path, exist_ok=True)
    osu_load_time = get_current_time()
    shutil.copyfile(pjoin(osu_root_path, "osu!.db"), pjoin(copy_db_path, "osu!.db"))
    shutil.copyfile(pjoin(osu_root_path, "collection.db"), pjoin(copy_db_path, "collection.db"))
    print("Copied.")

    print()
    print("Parsing databases...")
    osu_data = OsuDb.from_file(pjoin(copy_db_path, "osu!.db"))
    collection_data = OsuCollection.from_file(pjoin(copy_db_path, "collection.db"))
    print("Parsed.")

    print()
    print("osu!.db basic information: ")
    print(f"Version: {osu_data.osu_version}")
    print(f"Folders: {osu_data.folder_count}")
    print(f"Account unlocked: {osu_data.account_unlocked.value}")
    print(f"Unlock time: {osu_data.account_unlock_date}")
    print(f"Player name: {osu_data.player_name.value}")
    print(f"Beatmaps: {osu_data.num_beatmaps}")

    print()
    print("collection.db basic information:")
    print(f"Version: {collection_data.version}")
    print(f"Collections: {collection_data.num_collections}")

    """
    ## Commented for clear view
    print()
    print("Collections (beatmaps count):")
    for col in collection_data.collections:
        print(f"{col.name} ({col.num_beatmaps})")
    """

    print()
    print("Folders not in osu!.db:")
    db_folder_names = {bm.folder_name.value for bm in osu_data.beatmaps}
    for i in sorted(set(list_folders(osu_songs_path)) - db_folder_names):
        print(i)

    print()
    md5_count = len({bm.md5_hash.value for bm in osu_data.beatmaps})
    if md5_count != osu_data.num_beatmaps:  # collision
        print("MD5 collision found!")
        print(f"Beatmaps: {osu_data.num_beatmaps} / MD5: {md5_count}")
    else:
        print("No MD5 collision found.")

    print()
    print("Dump db to json to osudb.js...")
    with open(osudb_js_path, "w") as file:
        file.write("var osuLoaded = true;\n\n")
        file.write("var osudbJsLoaded = true;\n\n")
        file.write(f'var osuLoadTime = "{get_time_str(osu_load_time)}";\n\n')
        file.write(f'var osuSongsPath = {json.dumps("file://"+osu_songs_path)};\n\n')
        file.write(f"var osuSongs = {json.dumps(get_songs(osu_data.beatmaps))};\n\n")
        col_json = json.dumps(get_collections(osu_data.beatmaps, collection_data.collections))
        file.write(f"var osuCollections = {col_json};\n")

    playlist_collection = [
        col for col in collection_data.collections
        if col.name.value == playlist_collection_name]

    if playlist_collection:
        beatmaps_md5s = playlist_collection[0].beatmaps_md5s
        songs = get_songs_from_md5(get_md5_to_song_dict(osu_data.beatmaps), beatmaps_md5s)
        if playlist_shuffle:
            random.shuffle(songs)

        print()
        print(f"Dump collection to pls to {os.path.basename(pls_path)}...")
        with PLSWriter(pls_path, "w", encoding="utf-8", pretty_blank=True) as file:
            for song in songs:
                full_path = f'{osu_songs_path}/{song["folder"]}/{song["file"]}'
                file.write(full_path, song["title"], "%.3f" % (song["time"] / 1000))

        print()
        print(f"Dump collection to m3u to {os.path.basename(m3u_path)}...")
        with M3UWriter(m3u_path, "w", encoding="utf-8", pretty_blank=True) as file:
            for song in songs:
                full_path = f'{osu_songs_path}/{song["folder"]}/{song["file"]}'
                file.write(full_path, song["title"], "%.3f" % (song["time"] / 1000))

    print()
    input("Done!")
