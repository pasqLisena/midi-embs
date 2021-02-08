import os
from os import path
import shutil
import random

k = 10
root = '/Users/pasquale/Dropbox/musedata/midi'
dest_root = 'musedata_splitted'
all_files = []
dest_files = []

potset = [[] for i in range(0, 10)]
for folder in os.listdir(root):
    if folder == '.DS_Store' or folder.endswith('.zip'):
        continue

    filenames = [f for f in os.listdir(path.join(root, folder, 'midi1')) if f != '.DS_Store']
    random.shuffle(filenames)
    for i, filename in enumerate(filenames):
        pot = i % k
        potset[pot].append(path.join(folder, 'midi1', filename))

for j in range(k):
    for i, p in enumerate(potset):
        dr = path.join(dest_root, f'fold{j}', 'test' if i == j else 'train')
        for file in p:
            print(file, i, dr)
            folder = file.rsplit('/', 1)[0].replace('/midi1/', '/')
            os.makedirs(path.join(dr, folder), exist_ok=True)
            dst = path.join(dr, file.replace('/midi1/', '/'))
            src = path.join(root, file)
            shutil.copyfile(src, dst)
