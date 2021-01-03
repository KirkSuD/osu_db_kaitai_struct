#-*-coding:utf-8;-*-

from osu_db import OsuDb
from vlq_base128_le import VlqBase128Le

if __name__ == "__main__":
    ## simple testing code, set path accordingly before running

    ## your osu root path
    osu_root_path = r"%localappdata%/osu!"
    ## 2 folders to save output files
    output_json_path = r"./exported_json"
    output_serialized_path =  r"./serialized_db" ## should be completely same as original db

    import time, json, os, pickle

    def pkl_dump(obj, fpath):
        with open(fpath, "wb") as f:
            pickle.dump(obj, f)

    pjoin = os.path.join ## shortcut

    osu_root_path = os.path.expandvars(osu_root_path) ## https://stackoverflow.com/questions/53112401/percent-signs-in-windows-path
    osu_db_path = pjoin(osu_root_path, "osu!.db")
    collection_db_path = pjoin(osu_root_path, "collection.db")
    scores_db_path = pjoin(osu_root_path, "scores.db")

    output_json_path = os.path.abspath(os.path.realpath(output_json_path))
    osu_json = pjoin(output_json_path, "osu!.json")
    collection_json = pjoin(output_json_path, "collection.json")
    scores_json = pjoin(output_json_path, "scores.json")

    output_serialized_path = os.path.abspath(os.path.realpath(output_serialized_path))
    osu_serialized = pjoin(output_serialized_path, "osu!.db")
    collection_serialized = pjoin(output_serialized_path, "collection.db")
    scores_serialized = pjoin(output_serialized_path, "scores.db")

    input("Press ENTER...")

    st = time.time()
    res = OsuDb.from_file(osu_db_path)
    print(res.osu_version)
    
    print("Parsed osu!.db", time.time()-st)

    
