import numpy as np
from random import randint
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.preprocessing import LabelBinarizer
from sklearn.manifold import TSNE
from sklearn.preprocessing import normalize
from collections import Counter
import seaborn as sns


# source: https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues, print_values=True):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    # one hot to index
    y_true = [np.where(r == 1)[0][0] for r in y_true]
    # y_pred are already indexes

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = np.unique(classes)
    classes = classes[unique_labels(y_true, y_pred)]
    classes = [c[0:10] if len(c) > 10 else c for c in classes]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    fig, ax = plt.subplots(figsize=(8, 8))
    n = cm.shape[1]
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    # ax.figure.colorbar(im, ax=ax)

    # We want to show all ticks...
    ax.set(
        xticks=np.arange(n),
        yticks=np.arange(n),
        ylim=(n - 0.5, -0.5),
        # ... and label them with the respective list entries
        xticklabels=classes, yticklabels=classes,
        ylabel='True label',
        xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    if print_values:
        # Loop over data dimensions and create text annotations.
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

    fig.tight_layout()
    if normalize:
        title += '_norm'
    filename = 'plot/' + title + '.pdf'
    fig.savefig(filename, dpi=fig.dpi)


class OneHotEncoder:
    def __init__(self, labels):
        self.encoder = LabelBinarizer()
        self.labels = self.encoder.fit_transform(labels)

    def get(self, onehot):
        return self.encoder.inverse_transform(np.array([onehot]))[0]


def randcolor():
    return '#{:06x}'.format(randint(0, 256 ** 3))


def plot(vectors, labels, output='img.pdf'):
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(normalize(vectors))

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]

    plt.figure(figsize=(8, 8))
    sns.set(font_scale=1)
    sns.set_style("white")
    sns.scatterplot(
        x=x_coords, y=y_coords,
        hue=labels,
        palette=sns.color_palette("hls", len(np.unique(labels))),
        # data=df.loc[rndperm,:],
        legend="full",
        alpha=0.7
    )

    plt.savefig(output, dpi=2400)
    print('Picture saved at %s' % output)


def clean_and_filter(data, what, min_count=15, sort_by='value', plotting=True):
    """
    Remove the '?' items and keep only the ones
    with more than min_count occurrences
    """
    u = Counter(what)  # map label -> n. occurences

    enough_big = [(m not in ['?', '0'] and u[m] > min_count) for m in what]

    if type(data[0][0]) == np.ndarray:  # list of heterogeneous datasets
        data_filtered = [d[enough_big] for d in data]
    else:
        data_filtered = data[enough_big]
    what_filtered = what[enough_big]

    if sort_by == 'value':
        x = Counter(what_filtered).most_common()
    elif sort_by == 'key':
        x = sorted(Counter(what_filtered).items())
    else:
        x = Counter(what_filtered).items()

    labels, values = zip(*x)
    indexes = np.arange(len(labels))
    width = 1

    if plotting:
        plt.figure(figsize=(20, 6))
        plt.bar(indexes, values, width, align="center")
        plt.xticks(indexes - 1 + width, labels, rotation=45, horizontalalignment='right', rotation_mode='anchor')
        plt.show()

    return data_filtered, what_filtered


def extract_balanced(x, y, n_samples=30):
    """
    Create a well-balanced dataset containing n samples for each class.
    """

    pos = []
    for t in np.unique(y):
        indexes = np.where(y == t)[0]
        samples = np.random.choice(indexes, size=n_samples)
        pos.extend(samples)

    yy = y[pos]
    if type(x[0][0]) == np.ndarray:  # list of heterogeneous datasets
        xx = [d[pos] for d in x]
    else:
        xx = x[pos]

    return np.array(xx), np.array(yy)
