
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation
import numpy as np
from sklearn import svm
import pdb

def gbdt_model(trains):

    trains = np.array(trains)
    # cv = cross_validation.ShuffleSplit(trains.shape[0], n_iter=3, test_size=0.1, random_state=0)
    k_fold = cross_validation.KFold(n=trains.shape[0], n_folds=10)

    gbdt=GradientBoostingRegressor(
      loss='ls',
      learning_rate=0.1,
      n_estimators=100,
      subsample=1,
      min_samples_split=2,
      min_samples_leaf=1,
      max_depth=3,
      init=None,
      random_state=None,
      max_features=None,
      alpha=0.9,
      verbose=0,
      max_leaf_nodes=None,
      warm_start=False
    )


    train_set = trains[:, :-1]
    label_set = trains[:, -1]

    # predict_score = cross_validation.cross_val_score(gbdt, train_set, label_set, cv)
    # print predict_score
    # pdb.set_trace()
    score = cross_validation.cross_val_score(gbdt, train_set, label_set, cv=7, scoring='accuracy')

    print score


def svm_model(trains, fold):

    rbf_svm = svm.SVC(kernel='rbf', gamma=0.7, C=1)

    trains = np.array(trains)
    # cv = cross_validation.ShuffleSplit(trains.shape[0], n_iter=3, test_size=0.1, random_state=0)
    k_fold = cross_validation.KFold(n=trains.shape[0], n_folds=fold)


    train_set = trains[:, :-1]
    label_set = trains[:, -1]

    # predict_score = cross_validation.cross_val_score(gbdt, train_set, label_set, cv)
    # print predict_score
    # pdb.set_trace()
    score = cross_validation.cross_val_score(rbf_svm, train_set, label_set, cv=fold, scoring='accuracy')

    print score

if __name__ == '__main__':
    with open('test/traindata', 'r') as file:
        lines = file.readlines()
    pos_data = []
    neg_data = []
    for line in lines:
        datas = line.split(',')
        datas = map(lambda x:float(x), datas)
        if datas[-1] == 1:
            pos_data.append(datas)
        else:
            neg_data.append(datas)

    train_data = [data for data in pos_data]
    for data in neg_data:
        if np.random.randint(len(neg_data)) < len(pos_data):
            train_data.append(data)

    svm_model(train_data, 5)
