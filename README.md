# Learning MIDI embeddings

Repository in support to **MIDI2vec: Learning MIDI Embeddings for Reliable Prediction of Symbolic Music Metadata**.

> Pasquale Lisena, Albert Meroño-Peñuela, Raphaël Troncy. **MIDI2vec: Learning MIDI Embeddings for
> Reliable Prediction of Symbolic Music Metadata**, to appear in *Semantic Web Journal, Special Issue on Deep Learning for Knowledge Graphs*, 2021.
> http://www.semantic-web-journal.net/content/midi2vec-learning-midi-embeddings-reliable-prediction-symbolic-music-metadata-0

The experiment is available under 3 notebooks, covering 3 datasets:

- SLAC http://jmir.sourceforge.net/Codaich.html - [direct download](http://www.music.mcgill.ca/~cmckay/protected/SLAC_MIDI_Dataset.zip)
- Musedata http://old.musedata.org/ 
- Lakh https://colinraffel.com/projects/lmd/

The MIDI2vec library is available [here](https://github.com/midi-ld/midi2vec).

Pre-computed MIDI embeddings used in the paper are available in [Zenodo](https://zenodo.org/record/5082300).

# Embedding generation

Process to be performed for each `<dataset_folder>`.

- Clone [midi2vec repository](https://github.com/midi-ld/midi2vec) and enter in it
- Generate edgelists (absolute paths to prefer)
```
cd midi2edgelist
npm install
node index.js -i <dataset_folder>
node index.js -i <dataset_folder> -o edgelist_300 -n 300
```

- Compute embeddings
```
cd ../
pip install -r edgelist2vec/requirements.txt

python edgelist2vec/embed.py -o embeddings/<dataset>.bin
python edgelist2vec/embed.py -o embeddings/<dataset>_notes.bin --exclude notes
python edgelist2vec/embed.py -o embeddings/<dataset>_program.bin --exclude program
python edgelist2vec/embed.py -o embeddings/<dataset>_tempo.bin --exclude tempo
python edgelist2vec/embed.py -o embeddings/<dataset>_timesig.bin --exclude time.signature
python edgelist2vec/embed.py -i edgelist_300 -o embeddings/<dataset>_300.bin
```

- For SLAC and Musedata's CCV experimet, we use the script in `split_datasets` for splitting them in 10 folds
Then, for each fold `i`, the following commands need to be run
  
```
node index.js -i <dataset_splitted_folder>/fold<i>/train -o edgelist<i>
node index.js -i <dataset_splitted_folder>/fold<i>/test -o edgelist<i>_test

python edgelist2vec/embed.py -i edgelist<i> -o <dataset><i>.bin
```

# Classification experiment

- Copy the generated embedding files and edgelists (eventually from the pretrained zip files) in the relative dataset folder (together with the `.csv`) of midi-embs (this project)
- Open the following and run it:
    - SLAC: [classification-slac.ipynb](./classification-slac.ipynb)
    - Musedata: [classification-musedata.ipynb](./classification-musedata.ipynb)
    - Lakh: [classification-lakh.ipynb](./classification-lakh.ipynb)
