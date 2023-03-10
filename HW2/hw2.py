import math

import numpy as np
import pandas as pd

# data = np.genfromtxt('t.txt', dtype=int, encoding=None,delimiter=",")

#helper methods:
def splitter(D, index, value):
    D_y = []
    D_n = []
    for i in range(len(D[index])):
        if (D[index][i] <= value):
            D_y.append(D.iloc[i])
        else:
            D_n.append(D.iloc[i])
    return (D_y, D_n)

def wholeset_entropy(D, index):
    if len(D) == 0:
        return (0,0,0)

    D_y = []
    D_n = []
    # print(len(D[index]))
    for i in range(len(D[index])):
        if (D[10][i] == 1):
            D_y.append(D[index][i])
        else:
            D_n.append(D[index][i])

    if len(D_y) != 0 and len(D_n) != 0:
        whole_set_entropy = -(((len(D_y) / len(D)) * math.log2(len(D_y) / len(D)) + (len(D_n) / len(D)) * math.log2(len(D_n) / len(D))))

    elif len(D_y) == 0 and len(D_n) != 0:
        whole_set_entropy = -((0 + (len(D_n) / len(D)) * math.log2(len(D_n) / len(D))))

    elif len(D_y) != 0 and len(D_n) == 0:
        whole_set_entropy = -((0 + (len(D_y) / len(D)) * math.log2(len(D_y) / len(D))))

    Gini_index = 1 - (math.pow(((len(D_y) / len(D))), 2)) - (math.pow(((len(D_n) / len(D))), 2))

    # print(len(D_n))
    prob_difference = math.fabs(((len(D_y) / len(D))) - ((len(D_n) / len(D))))
    # print(prob_difference)

    return (whole_set_entropy,Gini_index, prob_difference)

#given methods
def IG(D, index, value):
    """Compute the Information Gain of a split on attribute index at value
    for dataset D.

    Args:
        D: a dataset, tuple (X, y) where X is the data, y the classes
        index: the index of the attribute (column of X) to split on
        value: value of the attribute at index to split at

    Returns:
        The value of the Information Gain for the given split
    """
    D_y = splitter(D,index, value)[0]
    D_n = splitter(D,index, value)[1]
    # print(len(D_y), len(D_n))
    # print("after split: D_y -- \n", pd.DataFrame(splitter(D,index, value)[0]))
    # print()
    # print("after split: D_n -- \n", pd.DataFrame(splitter(D,index, value)[1]))

    entropy_divide = (len(D_y)/len(D)) * wholeset_entropy(pd.DataFrame(D_y).reset_index(drop=True),index)[0] + (len(D_n)/len(D))  * wholeset_entropy(pd.DataFrame(D_n).reset_index(drop=True),index)[0]
    IG = wholeset_entropy(D, index)[0] - entropy_divide
    # print(entropy_divide)
    # print("found information gain: ", IG)
    return IG

#testing
# IG(data, 0, 1)

def G(D, index, value):
    """Compute the Gini index of a split on attribute index at value
    for dataset D.

    Args:
        D: a dataset, tuple (X, y) where X is the data, y the classes
        index: the index of the attribute (column of X) to split on
        value: value of the attribute at index to split at

    Returns:
        The value of the Gini index for the given split
    """
    D_y = splitter(D, index, value)[0]
    D_n = splitter(D, index, value)[1]

    if len(D_y) != 0 and len(D_n) != 0:
        gini_index = (len(D_y) / len(D)) * wholeset_entropy(pd.DataFrame(D_y).reset_index(drop=True), index)[1] + (len(D_n) / len(D)) * wholeset_entropy(pd.DataFrame(D_n).reset_index(drop=True), index)[1]

    elif len(D_y) != 0 and len(D_n) == 0:
        gini_index = (len(D_y) / len(D)) * wholeset_entropy(pd.DataFrame(D_y).reset_index(drop=True), index)[1]

    elif len(D_y) == 0 and len(D_n) != 0:
        gini_index = (len(D_n) / len(D)) * wholeset_entropy(pd.DataFrame(D_n).reset_index(drop=True), index)[1]

    # print("calculated gini index: ", gini_index)
    return gini_index

#testing
# G(data, 1, 28)


def CART(D, index, value):
    """Compute the CART measure of a split on attribute index at value
    for dataset D.

    Args:
        D: a dataset, tuple (X, y) where X is the data, y the classes
        index: the index of the attribute (column of X) to split on
        value: value of the attribute at index to split at

    Returns:
        The value of the CART measure for the given split
    """
    D_y = splitter(D,index,value)[0]
    D_n = splitter(D,index,value)[1]
    # print(len(D_y), len(D_n))
    cart = 2 * (len(D_y)/len(D)) * (len(D_n)/len(D)) * (wholeset_entropy(pd.DataFrame(D_y).reset_index(drop=True),index)[2] + wholeset_entropy(pd.DataFrame(D_n).reset_index(drop=True),index)[2])
    # print("Cart measure: ", cart)
    return cart

#testing
# CART(data,1,28)

def bestSplit(D, criterion):
    """Computes the best split for dataset D using the specified criterion

    Args:
        D: A dataset, tuple (X, y) where X is the data, y the classes
        criterion: one of "IG", "GINI", "CART"

    Returns:
        A tuple (i, value) where i is the index of the attribute to split at value
    """
    correspondingsplits = {}

    if(criterion.upper() == "IG"):
        print('chosen : IG')
        print()
        for i in D.columns[:10]:
            uniques = D[i].unique()
            for j in uniques:
                correspondingsplits[IG(D, i, j)] = (i,j)
        print("largest Information gain found: " , max(correspondingsplits), "with the attribute and value being", correspondingsplits.get(max(correspondingsplits)))
        return correspondingsplits.get(max(correspondingsplits))

    elif (criterion.upper() == "GINI"):
        print()
        print('chosen : GINI')
        print()

        for i in D.columns[:10]:
            uniques = D[i].unique()
            # print(uniques)
            for j in uniques:
                correspondingsplits[G(D, i, j)] = (i,j)
        print("smallest GINI found: ", min(correspondingsplits), "with the attribute and value being", correspondingsplits.get(min(correspondingsplits)))
        return correspondingsplits.get(min(correspondingsplits))

    elif (criterion.upper() == "CART"):
        print()
        print('chosen: CART')
        print()

        for i in D.columns[:10]:
            uniques = D[i].unique()
            for j in uniques:
                correspondingsplits[CART(D, i, j)] = (i,j)
        print("largest CART found: ", max(correspondingsplits), "with the attribute and value being", correspondingsplits.get(max(correspondingsplits)))
        return correspondingsplits.get(max(correspondingsplits))
    else:
        return (-1,-1)



# functions are first class objects in python, so let's refer to our desired criterion by a single name


def load(filename):
    """Loads filename as a dataset. Assumes the last column is classes, and
    observations are organized as rows.

    Args:
        filename: file to read

    Returns:
        A tuple D=(X,y), where X is a list or numpy ndarray of observation attributes
        where X[i] comes from the i-th row in filename; y is a list or ndarray of
        the classes of the observations, in the same order
    """
    data = pd.read_csv(filename, header=None)
    print("whole data: \n", data)
    print()
    # print(CART(data,0,1))
    best_IG = bestSplit(data, "IG")
    best_GINI = bestSplit(data, "GINI")
    best_CART = bestSplit(data, "CART")
    print()
    print("---------overall info----------")
    print("best IG at : ", best_IG)
    print("best GINI at : ", best_GINI)
    print("best CART at : ", best_CART)
    return (data, best_IG, best_GINI, best_CART)

#testing
# load('test.txt')

best_IG_fortrain = load('train.txt')

def classifyIG(train, test):
    """Builds a single-split decision tree using the Information Gain criterion
    and dataset train, and returns a list of predicted classes for dataset test

    Args:
        train: a tuple (X, y), where X is the data, y the classes
        test: the test set, same format as train

    Returns:
        A list of predicted classes for observations in test (in order)
    """
    data = pd.read_csv(test, header=None)
    # print(best_IG_fortrain[1])
    test_split = splitter(data, best_IG_fortrain[1][0], best_IG_fortrain[1][1])
    print()
    print("-------------------classification of IG------------------")
    print(pd.DataFrame(test_split[0]))
    print()
    print()
    print(pd.DataFrame(test_split[1]))
    # return

# classifyIG('train.txt', 'test.txt')

def classifyG(train, test):
    """Builds a single-split decision tree using the GINI criterion
    and dataset train, and returns a list of predicted classes for dataset test

    Args:
        train: a tuple (X, y), where X is the data, y the classes
        test: the test set, same format as train

    Returns:
        A list of predicted classes for observations in test (in order)
    """
    data = pd.read_csv(test, header=None)
    test_split = splitter(data, best_IG_fortrain[2][0], best_IG_fortrain[2][1])
    print()
    print("-------------------classification of G------------------")
    print(pd.DataFrame(test_split[0]))
    print()
    print()
    print(pd.DataFrame(test_split[1]))

# classifyG('train.txt', 'test.txt')

def classifyCART(train, test):
    """Builds a single-split decision tree using the CART criterion
    and dataset train, and returns a list of predicted classes for dataset test

    Args:
        train: a tuple (X, y), where X is the data, y the classes
        test: the test set, same format as train

    Returns:
        A list of predicted classes for observations in test (in order)
    """
    data = pd.read_csv(test, header=None)
    # print(best_IG_fortrain[1])
    test_split = splitter(data, best_IG_fortrain[3][0], best_IG_fortrain[3][1])
    print()
    print("-------------------classification of CART------------------")
    print(pd.DataFrame(test_split[0]))
    print()
    print()
    print(pd.DataFrame(test_split[1]))

# classifyCART('train.txt', 'test.txt')

def main():
    """This portion of the program will run when run only when main() is called.
    This is good practice in python, which doesn't have a general entry point
    unlike C, Java, etc.
    This way, when you <import HW2>, no code is run - only the functions you
    explicitly call.
    """
    classifyIG('train.txt', 'test.txt')
    classifyG('train.txt', 'test.txt')
    classifyCART('train.txt', 'test.txt')
    print()
    print()
    print()
    print()
    print("-------test original classification---------------")
    OG_test = load("test.txt")
    print("----------------IG based split -----------------")
    IGsplit = splitter(OG_test[0], OG_test[1][0],OG_test[1][1])
    print(pd.DataFrame(IGsplit[0]))
    print()
    print()
    print(pd.DataFrame(IGsplit[1]))
    print()
    print("----------------Gini based split -----------------")
    Gsplit = splitter(OG_test[0], OG_test[2][0], OG_test[2][1])
    print(pd.DataFrame(Gsplit[0]))
    print()
    print()
    print(pd.DataFrame(Gsplit[1]))
    print()
    print("----------------CART based split -----------------")
    Gsplit = splitter(OG_test[0], OG_test[3][0], OG_test[3][1])
    print(pd.DataFrame(Gsplit[0]))
    print()
    print()
    print(pd.DataFrame(Gsplit[1]))

if __name__ == "__main__":
    """__name__=="__main__" when the python script is run directly, not when it
    is imported. When this program is run from the command line (or an IDE), the
    following will happen; if you <import HW2>, nothing happens unless you call
    a function.
    """
    main()