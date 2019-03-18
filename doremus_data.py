import numpy as np
import codecs
import os
from gensim.models import KeyedVectors


def init(root_training, root_emb):
    global emb_dir, train_dir
    emb_dir = root_emb
    train_dir = root_training


def get_embeddings(what='expression'):
    vector_file = '%s/%s.emb' % (emb_dir, what)
    header_file = '%s/%s.emb.h' % (emb_dir, what)
    label_file = '%s/%s.emb.l' % (emb_dir, what)

    # load embeddings

    embedding = KeyedVectors.load_word2vec_format(vector_file)
    uris = np.array(embedding.index2entity)
    vectors = np.array([embedding.get_vector(k) for k in uris])
    vectors = np.ma.array(vectors, mask=-1. > vectors)

    lbs = np.array([line.strip() for line in codecs.open(label_file, 'r', 'utf-8').read().split('\n')[:-1]])
    try:
        heads = np.array([line.strip() for line in codecs.open(header_file, 'r', 'utf-8')])

        # header for printing
        head_label = heads[0].split()
        head_val = heads[1].split()
        head_dim = []
        for i in range(0, len(head_val)):
            for j in range(0, int(head_val[i])):
                head_dim.append(head_label[i])

        heads_print = [head_label, head_val]
    except FileNotFoundError:
        head_dim = None
        heads_print = None

    return vectors, uris, lbs, head_dim, heads_print


def all_training(what='expression'):
    return [{
        'name': 'pp_concerts',
        'playlists': _load_training('concerts/output/list/philharmonie', what)
    }, {
        'name': 'euterpe',
        'playlists': _load_training('concerts/output/list/euterpe', what)
    }, {
        #     'name': 'bnfbib',
        #     'playlists': _load_training('concerts/output/list/bnfbib', what)
        # }, {
        'name': 'itema3_concerts',
        'playlists': _load_training('concerts/output/list/itema3', what)
    }, {
        'name': 'web-radio',
        'playlists': _load_training('web-radio/output/list', what)
    }, {
        'name': 'spotify_pl',
        'playlists': _load_training('spotify/output/playlists/list', what)
    }]


def _load_training(sub, what='expression'):
    folder = os.path.join(train_dir, sub, what)
    playlists = []
    for f in sorted(os.listdir(folder)):
        file = '%s/%s' % (folder, f)
        data = np.array([line.strip() for line in codecs.open(file, 'r', 'utf-8')])
        playlists.append({
            'name': os.path.basename(file),
            'data': data
        })

    return playlists


