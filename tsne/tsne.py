import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE

sns.set()


def parse_args():
    parser = argparse.ArgumentParser(description="Run edgelist 2 vec.")

    parser.add_argument('-e', '--embeddings', required=True,
                        help='Input embeddings in gensim format.')

    parser.add_argument('-l', '--label', required=True,
                        help='Input label file in csv.')

    parser.add_argument('-d', '--dimensions', choices=[2, 3], default=2,
                        type=int, help='Num of dimensions.')

    parser.add_argument('--label-col', default='label',
                        help='Column from which take the label in the csv.')
    parser.add_argument('--id-col', default='id',
                        help='Column from which take the id in the csv.')

    parser.add_argument('-o', '--output', default='./output.eps',
                        help='Output EPS file.')

    parser.add_argument('--show', default=False, action='store_true',
                        help='Open the figure in a window')

    return parser.parse_args()


def main(args):
    print(args)
    df = pd.read_csv(args.label)
    embedding = KeyedVectors.load_word2vec_format(args.embeddings)

    ids = df[args.id_col].tolist()
    vectors = [embedding.get_vector(k) for k in ids]

    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=args.dimensions, random_state=0, n_iter=20000)
    Y = tsne.fit_transform(vectors)

    df['x'] = Y[:, 0]
    df['y'] = Y[:, 1]

    lbs = df[args.label_col].unique().tolist()

    # display scatter plot
    ax = plt.figure(figsize=(8, 8)).gca()
    if args.dimensions == 2:
        sns.scatterplot(
            x="x", y="y",
            hue=args.label_col,
            palette=sns.color_palette("hls", len(lbs)),
            data=df,
            legend="full",
            alpha=0.7)
    else:
        df['z'] = Y[:, 2]

        ax.gca(projection='3d')
        ax.scatter(
            xs=df["x"],
            ys=df["y"],
            zs=df["z"],
            c=[lbs.index(x) for x in df[args.label_col]],
            cmap='tab10')

    out = args.output
    plt.savefig(out, format='eps', dpi=1200)
    print('Picture saved at %s' % out)

    if args.show:
        plt.show()


if __name__ == '__main__':
    main(parse_args())
