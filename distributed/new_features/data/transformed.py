from collections import defaultdict
from scipy.sparse import csr_matrix
from distributed.new_features.utils.samplingNEW import NegativeSamplingFeat


# TrainSet
class TransformedSet(object):
    def __init__(self, user_indices=None, item_indices=None, labels=None, sparse_indices=None,
                 dense_values=None, train=True):
        self._user_indices = user_indices
        self._item_indices = item_indices
        self._labels = labels
        self._sparse_indices = sparse_indices
        self._dense_values = dense_values
        if train:
            self._sparse_interaction = csr_matrix((self.labels, (self.user_indices, self.item_indices)))
            self._train_user_consumed, self._train_item_consumed = self.__interaction_consumed()
        self.sparse_samples = None
        self.dense_samples = None
        self.label_samples = None

    def __interaction_consumed(self):
        train_user_consumed = defaultdict(list)
        train_item_consumed = defaultdict(list)
        for u, i in zip(self.user_indices, self.item_indices):
            train_user_consumed[u].append(i)
            train_item_consumed[i].append(u)
        return train_user_consumed, train_item_consumed

    def build_negative_samples(self, data_info, num_neg=1, seed=42):
        neg_generator = NegativeSamplingFeat(self, data_info, num_neg)
        if self.dense_values is None:
            self.sparse_samples, self.label_samples = neg_generator(seed, dense=False)
        else:
            self.sparse_samples, self.dense_samples, self.label_samples = neg_generator(seed, dense=True)

    def __len__(self):
        return len(self.sparse_indices)

    @property
    def user_indices(self):
        return self._user_indices

    @property
    def item_indices(self):
        return self._item_indices

    @property
    def sparse_indices(self):
        return self._sparse_indices

    @property
    def dense_values(self):
        return self._dense_values

    @property
    def labels(self):
        return self._labels

    @property
    def sparse_interaction(self):
        return self._sparse_interaction

    @property
    def train_user_consumed(self):
        return self._train_user_consumed

    @property
    def train_item_consumed(self):
        return self._train_item_consumed


class TestSet:
    def __init__(self, labels, sparse_indices, dense_values=None, mode="pure"):
        self.sparse_indices = sparse_indices
        self.dense_values = dense_values
        self.labels = labels
        self.mode = mode
        self.sparse_indices_plus_neg = None
        self.dense_values_plus_neg = None

    def build_negative(self, num_neg=1, item_feat_cols=None):
        pass

    def user_indices(self, data_info):
        pass

    def item_indices(self, data_info):
        """indices used for construct embedding"""
        pass

    @property
    def sparse_indices(self):
        return self.sparse_indices

    @property
    def dense_values(self):
        return self.dense_values