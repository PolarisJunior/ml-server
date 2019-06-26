
import numpy as np
from ml_modules.ml_base import MlBase

class KMeans(MlBase):
    algo_id = 1
    
    def __init__(self, data, args):
        print("Constructed KMeans")
        self.data = data
        self.k = 1
        self.dims = 1

        if "k" in args:
            self.k = args["k"]

        if "dims" in args:
            self.dims = args["dims"]

        self.cluster_mappings = -np.ones(len(self.data))

    def init_means(self):
        indices = np.random.randint(0, len(self.data), size=self.k)
        self.means = np.array([self.data[i] for i in indices])

    def assign_clusters(self):
        new_means = np.zeros((self.k, self.dims))

        cluster_counts = np.zeros(self.k)
        num_changed = 0
        for i in range(0, len(self.data)):
            sample = self.data[i]
            cluster_id = int(self.assign_cluster(sample))

            if self.cluster_mappings[i] != cluster_id:
                num_changed += 1

            self.cluster_mappings[i] = cluster_id
            cluster_counts[cluster_id] += 1
            new_means[cluster_id] += self.data[i]

        self.means = np.true_divide(new_means.transpose(), cluster_counts).transpose()
        return num_changed

    def assign_cluster(self, sample):
        # calculate distance from each mean cluster
        dists = [np.sum((mu - sample) ** 2) for mu in self.means]
        return np.argmin(dists)

    def calc_means(self):
        pass

    def run(self):
        self.init_means()
        # lloyd algorithm
        while self.assign_clusters() > 0:
            self.calc_means()
        return self.means
    pass