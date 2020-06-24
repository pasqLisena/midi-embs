# Learning MIDI embeddings

Repository in support to **MIDI2vec: Learning MIDI Embeddings for Reliable Prediction of Symbolic Music Metadata**.

The experiment is available under 3 notebooks, covering 3 datasets:

- SLAC http://jmir.sourceforge.net/Codaich.html
- Musedata http://old.musedata.org/
- Lakh https://colinraffel.com/projects/lmd/

# Embedding generation

Process to be performed for each `<dataset_folder>`.

- Clone midi2vec repository and enter in it
- Generate edgelists
```
cd midi2edgelist
npm install
node index.js -i <dataset_folder>
```
- Compute embeddings
```
cd ../
pip install -r edgelist2vec/requirements.txt

python edgelist2vec/embed.py -o embeddings/<dataset>.emb
```

# Classification experiment

- Copy the generated embedding file in the relative dataset folder (together with the `.csv`) of midi-embs
- Open the notebook `classification-<dataset>` and run it
