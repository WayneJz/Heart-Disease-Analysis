from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt

from machine_learning.feature_selection import FeatureSelection


class MultiClassifier:
    def __init__(self, target_num=5):
        # KNN classifier
        self.knn = KNeighborsClassifier(n_neighbors=target_num)
        self.data = pd.read_csv('../data/pandas_cleaned.csv')

        selection = FeatureSelection(self.data)
        self.top_important_factors = selection.correlation()

        self.training_target = None
        self.test_target = None
        self.training_data = None
        self.test_data = None

        self.model = None

    def train_test_splitter(self, ratio, random_seed=1000):
        train_data = self.data.sample(frac=ratio, random_state=random_seed)
        test_data = self.data.drop(train_data.index)
        self.training_target = train_data.filter(['target'])
        self.test_target = test_data.filter(['target'])

        selected_train = train_data.filter(self.top_important_factors)
        select_test = test_data.filter(self.top_important_factors)

        # Minmax normalization
        self.training_data = (selected_train - selected_train.min()) / (selected_train.max() - selected_train.min())
        self.test_data = (select_test - select_test.min()) / (select_test.max() - select_test.min())

    def model_fitting(self):
        data = [_ for _ in self.training_data.values.tolist()]
        target = [int(_[0]) for _ in self.training_target.values.tolist()]
        self.knn.fit(data, target)

    def accuracy(self):
        test_result = self.knn.predict(self.test_data)
        test_target = [int(_[0]) for _ in self.test_target.values.tolist()]
        accurate_count = 0
        for i in range(len(test_result)):
            if test_result[i] == test_target[i]:
                accurate_count += 1
        accuracy = accurate_count / len(test_target)
        print('Accuracy: ', accuracy)
        return accuracy

    def run(self):
        percentage_list = list()
        accuracy_list = list()
        for i in range(10, 90):
            self.train_test_splitter(i / 100)
            self.model_fitting()
            percentage_list.append(i)
            accuracy_list.append(self.accuracy())
        plt.plot(percentage_list, accuracy_list)
        plt.title('KNN Multi Classifier')
        plt.xlabel('Percentages of training data %')
        plt.ylabel('Accuracy')
        plt.savefig('../data/KNN.png')
        plt.show()

    def predict(self, input_data):
        self.train_test_splitter(0.9)
        self.model_fitting()
        return self.knn.predict(input_data)


if __name__ == "__main__":
    classifier = MultiClassifier()
    classifier.run()