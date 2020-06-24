import os
from os import path
import h5py
import pandas
import json
import shutil
from tqdm import tqdm

hdf5_folder = '/Users/pasquale/MIDI stuff/lmd_matched_h5/'
midi_folder = '/Users/pasquale/MIDI stuff/lmd_matched/'
out_csv = '../lakh/lakh2.csv'
out_midi = '../lakh/lmd_subset/'
os.makedirs(out_midi, exist_ok=True)

with open('match_scores.json') as json_file:
    scores = json.load(json_file)


def read_hdf5(file_path):
    id = file_path.replace(hdf5_folder, '').replace('.h5', '')
    msd_id = id.split('/')[-1]
    item = {'id': msd_id}

    with h5py.File(file_path, 'r') as f:  # open file

        item['year'] = f['musicbrainz/songs'][0][1]

        item['tag_echo'] = ''
        item['tag_mbz'] = ''
        tags_echo = f['metadata/artist_terms'][:]
        if len(tags_echo) > 0:
            item['tag_echo'] = tags_echo[0].decode()

        tags_mbz = f['musicbrainz/artist_mbtags'][:]
        if len(tags_mbz) > 0:
            item['tag_mbz'] = tags_mbz[0].decode()

        song = f['metadata/songs'][0]
        item['artist_mb'] = song[8].decode()
        item['artist_name'] = song[9].decode()
        item['album_name'] = song[14].decode()
        item['song_name'] = song[18].decode()

        candidates = scores[msd_id]
        best = None
        score = 0
        for key, value in candidates.items():
            if value > score:
                best = key
                score = value

        file = path.join(id, best + '.mid')
        shutil.copyfile(path.join(midi_folder, file), path.join(out_midi, msd_id + '.mid'))
        item['file'] = file

        return item


df = pandas.DataFrame(
    columns=['id', 'file', 'song_name', 'album_name', 'artist_name', 'artist_mb', 'tag_echo', 'tag_mbz', 'year'])

file_list = [path.join(root, name) for root, dirs, files in os.walk(hdf5_folder, topdown=False) for name in files]

for f in tqdm(file_list):
    df = df.append(read_hdf5(f), ignore_index=True)

df.to_csv(out_csv, index_label=False)
