import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"C:\Users\ADITYA\Downloads\Salary_Data.csv")

x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state= 0)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train , y_train)

y__pred = regressor.predict(x_test)

comparison = pd.DataFrame({'Actual': y_test, 'predicted': y__pred})
print(comparison)

plt.scatter(x_test, y_test, color = 'red')
plt.plot(x_train, regressor.predict(x_train), color='blue')
plt.title('Salary vs Experience (Test set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()


m = regressor.coef_
print(m)

c = regressor.intercept_
print(c)

y_12 = m * 12 + c
print(y_12)

y_20 = m * 20 + c
print(y_20)

y_10 = m * 10 + c
print(y_10)

x_10 = m * 15 + c
print(x_10)

exp_12_future_pred = 9312*12+26780
exp_12_future_pred


bias = regressor.score(x_train, y_train)
print(bias)

variance = regressor.score(x_test, y_test)
print(variance)

dataset.mean()

dataset['Salary'].mean()

dataset.median()

dataset['Salary'].median()

dataset.mode()

dataset['Salary'].mode()

dataset.var()

dataset['Salary'].var()

dataset.std()

dataset['Salary'].std()

from scipy.stats import variation

variation(dataset.values)

variation(dataset['Salary'])

dataset.corr()

dataset['Salary'].corr(dataset['YearsExperience'])

dataset.skew()

dataset['Salary'].skew()

dataset.sem()  # this will standard error of entire dataframe

dataset['Salary'].skew()

import scipy.stats as stats
dataset.apply(stats.zscore)

stats.zscore(dataset['Salary'])

y_mean = np.mean(y)
SSR = np.sum((y__pred-y_mean)**2)
print(SSR)

y = y[0:6]
SSE = np.sum((y-y__pred)**2)
print(SSE)

mean_total = np.mean(dataset.values)

SST = np.sum((dataset.values-mean_total)**2)
print(SST)

r_square = 1 - (SSR/SST)
r_square

from sklearn.metrics import mean_squared_error
train_mse = mean_squared_error(y_train, regressor.predict(x_train))
test_mse = mean_squared_error(y_test, y__pred)

print(train_mse)
print(test_mse)

import pickle
filename = 'linear_regression_model.pkl'
with open(filename, 'wb') as file:
    pickle.dump(regressor, file)
print("model has been pickled and saved has linear_regression model")
import os
print(os.getcwd())



