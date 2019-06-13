import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def normalize(X):
    '''
    Given a design matrix, X, normalizes each feature's values
    To be in the range -0.5 <= x <= 0.5 (aprrox)
    The formula used for normalization is:
        X = (X - mean) / (Standard deviation)

    This prevents overflow warnings from NumPy

    Arguments:
        X: ndarray, (m, n) matrix consisting of the features

    Returns:
        X: ndarray, (m, n) normalized matrix with the features
    '''

    # Since each feature is stored column-wise, axis=0
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)

    return (X - mu) / sigma


def load_data(path):
    '''
    Given a CSV file as path, extracts:
        * The design matrix
        * The y-values
        * The number of training examples
        * The number of features

    Assumes that all columns of the CSV file except the last one has features
    And the last column has y-values
    If there are x columns leaving the last column in the data, an extra
    feature is added to have x+1 features (x_0 = 1 for all training egs)
    So that the intercept term can be treated as another parameter

    Also, creates a matrix, theta, with initial value of parameters

    Arguments:
        path: str, the path of the CSV file

    Returns: (X, y, theta, m, n): tuple, consisting:
        m: int, number of training examples
        n: int, number of features (= x + 1, including x_0)
        X: ndarray, (m, n) matrix consisting of the features
        y: ndarray, (m, 1) matrix consisting of y-values
        theta: ndarray, (n, 1) zero matrix for initial parameters
    '''
    data = pd.read_csv(path, header=None)
    m = data.shape[0]

    # Getting values of features
    X = np.array(data.iloc[:, 0:-1])

    # Normalizing the features if there are more than one feature
    if X.shape[1] > 1:
        X = normalize(X)

    # Appending (m, 1) matrix of ones for extra feature x_0
    # Each row of matrix corresponds to a training example
    # Each column corresponds to a feature
    X = np.append(np.ones((m, 1)), X, axis=1)

    # Getting y values as (m, 1) matrix
    y = np.reshape(np.array(data.iloc[:, -1]), (m, 1))

    # Initializing theta to a (n, 1) zero matrix
    # n is the number of features
    n = X.shape[1]
    theta = np.zeros((n, 1))

    return X, y, theta, m, n


def cost_function(X, y, theta, m):
    '''
    Calculates the value of the cost function
    For a given X, y, theta and m

    The formula for the cost function is as follows:

        cost, J = (1/2 * m) * sum((X * theta - y) ^ 2)

    Arguments:
        X: ndarray, (m, n) matrix consisting of the features
        y: ndarray, (m, 1) matrix with y-values
        theta: ndarray, (n, 1) matrix with parameter values
        m: int, number of training examples

    Returns:
        J: ndarray, (1,1) matrix with value of cost function
    '''
    predictions = X @ theta
    sqr_err = np.square(predictions - y)
    return 1 / (2 * m) * sum(sqr_err)


def plot_cost(costs):
    '''
    Plots the values of the cost function
    Against number of iterations
    If gradient descent has converged, graph flattens out
    And becomes constant near the final iterations
    Otherwise, it shows a different trend
    '''
    plt.plot(costs)
    plt.xlabel("Number of iterations")
    plt.ylabel("J(theta)")
    plt.title("Iterations vs Cost")
    plt.show()


def gradient_descent(X, y, theta, alpha, num_iters, m):
    '''
    Runs gradient descent num_iters times
    To get the optimum values of the parameters
    The algorithm can be looked at here:
    https://en.wikipedia.org/wiki/Gradient_descent

    It can be vectorized as follows:
        theta = theta - (alpha / m) * ((X * theta - y)' * X)'

    Arguments:
        X: ndarray, (m, n) matrix consisting of the features
        y: ndarray, (m, 1) matrix with y-values
        theta: ndarray, (n, 1) matrix with initial parameter values
        alpha: float, the learning rate
        num_iters: int, the number of times algorithm is to be run
        m: int, the number of training examples

    Returns:
        theta: ndarray, (n, 1) matrix with optimum param values
    '''

    # Array to store cost values at each iteration
    # Will be used to check convergence of the algorithm
    j_vals = np.zeros((num_iters, 1))

    for i in range(num_iters):
        # (X * theta - y)'
        difference = np.transpose((X @ theta - y))
        # ((X * theta - y) * X)'
        delta = np.transpose(difference @ X)
        theta = theta - (alpha / m) * delta
        j_vals[i][0] = cost_function(X, y, theta, m)

    # Plotting the cost values
    plot_cost(j_vals)
    return theta
