import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")



def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - 0Administrative, an integer1
        - 1Administrative_Duration, a floating point number1
        - 2Informational, an integer1
        - 3Informational_Duration, a floating point number1
        - 4ProductRelated, an integer1
        - 5ProductRelated_Duration, a floating point number1
        - 6BounceRates, a floating point number1
        - 7ExitRates, a floating point number1
        - 8PageValues, a floating point number1
        - 9SpecialDay, a floating point number
        - 10Month, an index from 0 (January) to 11 (December)
        - 11OperatingSystems, an integer
        - 12Browser, an integer
        - 13Region, an integer
        - 14TrafficType, an integer
        - 15VisitorType, an integer 0 (not returning) or 1 (returning)
        - 16Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    with open(filename, 'r') as csvfile:
        month_to_num = {
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "Apr": 3,
            "May": 4,
            "June": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11
        }

        def returning_user(input):
            if input == 'Returning_Visitor':
                return 1
            else:
                return 0
            
        def bool_to_num(bool):
            if bool == 'FALSE':
                return 0
            else:
                return 1
        
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        evidence = []
        labels = []
        for row in csvreader:
           evidence_add = [int(row[0]),float(row[1]),int(row[2]),float(row[3]),int(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),
                           float(row[9]),int(month_to_num[row[10]]), int(row[11]),int(row[12]),int(row[13]),int(row[14]),returning_user(row[15]), bool_to_num(row[16])]
           evidence.append(evidence_add)
           labels.append(bool_to_num(row[17]))
           

    return (evidence, labels)   
 

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    holdout = TEST_SIZE * len(evidence)
    model.fit(evidence, labels)
    return model
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_predicted = 0
    negative_predicted = 0
    positive_correct = 0
    negative_correct = 0

    for index in range(len(predictions)):
        if predictions[index] == 1:
            positive_predicted+=1
            if labels[index] == 1:
                positive_correct+=1
        elif predictions[index] == 0:
            negative_predicted+=1
            if labels[index] == 0:
                negative_correct+=1

    print(f'Predicted Positive Values: {positive_predicted}')
    print(f'Actual Positive Values {positive_correct}')
    sensitivity = float(positive_correct/positive_predicted)
    specificity = float(negative_correct/negative_predicted)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
