# Learning MIDI embeddings

Repository in support to **MIDI2vec: Learning MIDI Embeddings for Reliable Prediction of Symbolic Music Metadata**.

The experiment is available under 3 notebooks, covering 3 datasets:

- SLAC http://jmir.sourceforge.net/Codaich.html - [direct download](http://www.music.mcgill.ca/~cmckay/protected/SLAC_MIDI_Dataset.zip)
- Musedata http://old.musedata.org/ 
- Lakh https://colinraffel.com/projects/lmd/

Datasets (original and splitted) and all trained models are available at https://www.doremus.org/midi/

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
