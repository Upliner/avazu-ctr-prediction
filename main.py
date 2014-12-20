# id: ad identifier
# click: 0/1 for non-click/click
# hour: format is YYMMDDHH, so 14091123 means 23:00 on Sept. 11, 2014 UTC.
# C1 -- anonymized categorical variable
# banner_pos
# site_id
# site_domain
# site_category
# app_id
# app_domain
# app_category
# device_id
# device_ip
# device_model
# device_type
# device_conn_type
# C14-C21 -- anonymized categorical variables

import pandas as pd
from pandas.util.testing import DataFrame
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def load_df(filename):
    df = pd.read_csv(filename, header=0)
    df = df.drop(['id', 'site_id', 'app_id', 'device_id', 'device_ip', 'site_domain',
                  'site_category', 'app_domain', 'app_category', 'device_model'], axis=1)
    return df.values


def print_metrics(true_values, predicted_values):
    print "Accuracy: ", metrics.accuracy_score(true_values, predicted_values)
    print "AUC: ", metrics.roc_auc_score(true_values, predicted_values)
    print "Confusion Matrix: ", + metrics.confusion_matrix(true_values, predicted_values)
    print metrics.classification_report(true_values, predicted_values)


def create_submission(predictions, filename='submission.csv'):
    df = DataFrame(predictions)
    df.to_csv(filename, header=['click'])


def classify(classifier_class, train_input, train_targets):
    classifier_object = classifier_class()
    classifier_object.fit(train_input, train_targets)
    return classifier_object


train_data = load_df('csv/train_small.csv')

# 'id' column should be merged back into train and test data
X_train, X_test, y_train, y_test = train_test_split(train_data[0::, 1::], train_data[0::, 0],
                                                    test_size=0.3, random_state=0)

classifier = classify(LogisticRegression, X_train, y_train)
predictions = classifier.predict(X_test)
print_metrics(y_test, predictions)
create_submission(predictions)


