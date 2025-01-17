from osu_db import osu_db
from osu_collection import osu_collection
from osu_scores import osu_scores


class PLSWriter:
    def __init__(self, *args, **kwargs):
        self.file = open(*args, **kwargs)
        self.file.write("[playlist]\n\n")
        self.num_entries = 0

    def write(self, file, title=None, length=None):
        self.num_entries += 1
        self.file.write("File%d=%s\n" % (self.num_entries, file))
        if title is not None:
            self.file.write("Title%d=%s\n" % (self.num_entries, title))
        if length is not None:
            self.file.write("Length%d=%s\n" % (self.num_entries, length))
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
    def __init__(self, *args, **kwargs):
        self.file = open(*args, **kwargs)
        self.file.write("#EXTM3U\n\n")

    def write(self, file, title=None, length=None):
        if title is not None or length is not None:
            self.file.write("#EXTINF:")
            if length is not None:
                self.file.write("%s," % length)
            if title is not None:
                self.file.write("%s" % title)
        self.file.write("\n%s\n\n" % file)

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == "__main__":
    import argparse
    from path_util import canonical_path, get_osu_dir, replace_invalid_filename

    parser = argparse.ArgumentParser(
        description="Convert osu! collections to playlists",
    )
    parser.add_argument(
        "-s", "--source",
        help="osu! directory (default: platform specific)"
    )
    parser.add_argument(
        "-d", "--destination",
        default="./osu_collection_playlist",
        help="Destination directory (default: ./osu_collection_playlist)"
    )
    parser.add_argument(
        "-c", "--collections",
        nargs="*",
        help="Collections to convert (default: all)"
    )
    parser.add_argument(
        "-p", "--prefix",
        help="Songs directory (default: platform specific)"
    )
    parser.add_argument(
        "-u", "--unicode",
        action="store_true",
        default=False,
        help="Use unicode title (default: false)"
    )
    parser.add_argument(
        "-m", "--m3u",
        action="store_true",
        default=False,
        help="Output .m3u8 instead of .pls (default: .pls)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        default=False,
        help="Hide errors & warnings (default: print)"
    )
    args = parser.parse_args()
    print("Raw arguments:", args)

    source = args.source
    if source is None:
        source = get_osu_dir()
    else:
        source = canonical_path(source)
    destination = canonical_path(args.destination)
    if not destination.is_dir():
        destination.mkdir()

    wanted_collections = args.collections
    prefix = args.prefix
    if prefix is None:
        prefix = str(source / "Songs") + "/"
    unicode_title = args.unicode
    m3u = args.m3u
    quiet = args.quiet

    print("Processed args:")
    print(f"{source=}")
    print(f"{destination=}")
    print(f"{wanted_collections=} (None means ALL)")
    print(f"{prefix=}")
    print(f"{unicode_title=}")
    print(f"{m3u=}")
    print(f"{quiet=}")

    print()
    print("Parsing DBs from:", source)
    osu_data = osu_db.parse_file(source / "osu!.db")
    collection_data = osu_collection.parse_file(source / "collection.db")
    scores_data = osu_scores.parse_file(source / "scores.db")

    print()
    print(
        f"osu!.db: v{osu_data.osu_version}",
        f"{osu_data.folder_count} folders",
        f"{len(osu_data.beatmaps)} beatmaps"
    )
    print(
        f"collection.db: v{collection_data.version}",
        f"{len(collection_data.collections)} collections"
    )
    print(
        f"scores.db: v{scores_data.version}",
        f"{len(scores_data.beatmaps)} beatmaps",
        f"{sum(len(bm.scores) for bm in scores_data.beatmaps)} scores",
    )

    collections = {
        c.name: c.beatmaps_md5s
        for c in collection_data.collections
        if wanted_collections is None or c.name in wanted_collections
    }
    beatmaps = {bm.md5_hash: bm for bm in osu_data.beatmaps}
    print()
    print("Converting collections to:", destination)

    for collection_name, collection_hashes in collections.items():
        print()
        print("Collection:", collection_name)
        folders = set()
        writer = M3UWriter if m3u else PLSWriter
        filename = replace_invalid_filename(collection_name)
        filename += ".m3u8" if m3u else ".pls"
        with writer(destination / filename, "w", encoding="utf-8") as playlist:
            for h in collection_hashes:
                if h not in beatmaps:
                    if not quiet:
                        print("Error: md5 hash not found in beatmaps:", h)
                    continue

                bm = beatmaps[h]
                folder = bm.folder_name
                file = bm.audio_file_name
                title = bm.song_title_unicode if unicode_title else bm.song_title
                length = f"{bm.total_time / 1000:.3f}"
                if folder in folders:
                    continue
                folders.add(folder)

                if not quiet and not (source / "Songs" / folder).is_dir():
                    print("Warning: folder not found:", folder)
                elif not quiet and not (source / "Songs" / folder / file).is_file():
                    print("Warning: file not found:", folder, file)
                playlist.write(prefix + folder + "/" + file, title, length)
        print(len(folders), "songs")
