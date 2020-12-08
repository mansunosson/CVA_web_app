# Import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.neural_network
import sklearn.linear_model
import sklearn.model_selection
import sklearn.metrics
import sklearn.preprocessing
import pickle
import keras
import os

# Load corporate default data
defaultdata = pd.read_csv("corporate_default_data.csv").dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

# Print unconditional default rate in data
defaultdata = defaultdata.iloc[range(3300),:] # Drop some rows with DEF = 1 due to biased sampling
print('The unconditional default rate in data is: ' + str(np.mean(defaultdata['DEF']))) # Note: a default rate of 0.25, due to biased sampling, is likely to skew the results of the model

# Split data set in train and test
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(defaultdata.drop("DEF", axis = 1), defaultdata.pop("DEF"), test_size=0.2, random_state=5, stratify=Y)

# Define wrapper function for Logistic regression
def logreg_train(X_train, Y_train, X_test, Y_test):
    
    # Create logistic regression model object
    classifier = sklearn.linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0,
                                            fit_intercept=False, intercept_scaling=1, class_weight=None, 
                                            random_state=None, solver='lbfgs', max_iter=1000, multi_class='auto', 
                                            verbose=0, warm_start=False, n_jobs=None, l1_ratio=None)
    
    # Fit classifier using the training data
    classifier.fit(X_train, Y_train)
    # Save model object to disk
    pickle.dump(classifier, open('pd_model.sav', 'wb'))
    
    # Evaluate on training data
    print('\n-- Training data --')
    pred = classifier.predict(X_train)
    accuracy = sklearn.metrics.accuracy_score(Y_train, pred)
    print('Accuracy: {0:.2f}'.format(accuracy * 100.0))
    print('Classification Report:')
    print(sklearn.metrics.classification_report(Y_train, pred))
    print('Confusion Matrix:')
    print(sklearn.metrics.confusion_matrix(Y_train, pred))
    print('')
    # Evaluate on test data
    print('\n---- Test data ----')
    pred = classifier.predict(X_test)
    accuracy = sklearn.metrics.accuracy_score(Y_test, pred)
    print('Accuracy: {0:.2f}'.format(accuracy * 100.0))
    print('Classification Report:')
    print(sklearn.metrics.classification_report(Y_test, pred))
    print('Confusion Matrix:')
    print(sklearn.metrics.confusion_matrix(Y_test, pred))
    print('Coefficients:')
    coefs = pd.DataFrame(data = classifier.coef_, columns = list(X_train.columns))
    print(coefs)

# Evaluate the model
logreg_train(X_train, Y_train, X_test, Y_test)











