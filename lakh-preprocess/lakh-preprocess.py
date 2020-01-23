import os
import h5py
import pandas
import json

source = '/Users/pasquale/Downloads/lmd_matched_h5/A/A/A'
out = '../embeddings/'

with open('match_scores.json') as json_file:
    scores = json.load(json_file)


def read_hdf5(path):
    item = {'id': path.replace(source, '').replace('.h5', '')}
    msd_id = item['id'].split('/')[-1]

    print(item['id'])
    with h5py.File(path, 'r') as f:  # open file

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

        item['file'] = best
        print(item['file'])
        return item


df = pandas.DataFrame(
    columns=['id', 'file', 'song_name', 'album_name', 'artist_name', 'artist_mb', 'tag_echo', 'tag_mbz', 'year'])

for root, dirs, files in os.walk(source, topdown=False):
    for name in files:
        df = df.append(read_hdf5(os.path.join(root, name)), ignore_index=True)

# df.set_index('id', inplace=True)

df.to_csv(out + 'lakh.csv')

# with open(out + 'echo.txt', 'w') as f:
#     f.write('\n'.join(df['tag_echo'].tolist()))
# with open(out + 'mbz.txt', 'w') as f:
#     f.write('\n'.join(df['tag_mbz'].tolist()))
# with open(out + 'years.txt', 'w') as f:
#     f.write('\n'.join(df['year'].astype(np.str).tolist()))
# with open(out + 'ids.txt', 'w') as f:
#     f.write('\n'.join(df['id'].tolist()))
