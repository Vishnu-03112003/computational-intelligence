import math
import pandas as pd

from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# ----------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------

def entropy(data):
    total = len(data)
    counts = Counter(data)
    ent = 0
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent


def gini(data):
    total = len(data)
    counts = Counter(data)
    g = 1
    for count in counts.values():
        p = count / total
        g -= p ** 2
    return g


# ----------------------------------------------------------
# SINGLE GAIN FUNCTION (Entropy / Gini)
# ----------------------------------------------------------

def gain(dataset, attribute, target, criterion):
    target_values = [row[target] for row in dataset]

    if criterion == "entropy":
        parent = entropy(target_values)
        print(f"\nParent Entropy = {parent:.4f}")
    else:
        parent = gini(target_values)
        print(f"\nParent Gini = {parent:.4f}")

    values = set(row[attribute] for row in dataset)
    weighted_impurity = 0

    for val in values:
        subset = [row for row in dataset if row[attribute] == val]
        subset_targets = [row[target] for row in subset]
        weight = len(subset) / len(dataset)

        if criterion == "entropy":
            impurity = entropy(subset_targets)
            print(f"Entropy({attribute}={val}) = {impurity:.4f}")
        else:
            impurity = gini(subset_targets)
            print(f"Gini({attribute}={val}) = {impurity:.4f}")

        weighted_impurity += weight * impurity

    gain_value = parent - weighted_impurity
    print(f"{criterion.capitalize()} Gain({attribute}) = {gain_value:.4f}")
    return gain_value


# ----------------------------------------------------------
# Manual Decision Tree (ID3 / CART style)
# ----------------------------------------------------------

def build_tree(dataset, attributes, target, criterion):
    target_values = [row[target] for row in dataset]

    if len(set(target_values)) == 1:
        return target_values[0]

    if not attributes:
        return Counter(target_values).most_common(1)[0][0]

    gains = {}
    print("\nEvaluating attributes:")
    for attr in attributes:
        gains[attr] = gain(dataset, attr, target, criterion)

    best_attr = max(gains, key=gains.get)
    print(f"\nSelected Best Attribute: {best_attr}")

    tree = {best_attr: {}}
    values = set(row[best_attr] for row in dataset)

    for val in values:
        subset = [row for row in dataset if row[best_attr] == val]
        remaining_attrs = [a for a in attributes if a != best_attr]
        tree[best_attr][val] = build_tree(subset, remaining_attrs, target, criterion)

    return tree


def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "->", tree)
        return

    for attr, branches in tree.items():
        for val, subtree in branches.items():
            print(f"{indent}{attr} = {val}")
            print_tree(subtree, indent + "   ")


def predict(tree, sample):
    if not isinstance(tree, dict):
        return tree

    attr = next(iter(tree))
    value = sample.get(attr)

    if value in tree[attr]:
        return predict(tree[attr][value], sample)
    else:
        return "Unknown"


# ----------------------------------------------------------
# Manual Mode
# ----------------------------------------------------------

def manual_mode(criterion):
    n_attr = int(input("Enter number of attributes (excluding target): "))
    attributes = input("Enter attribute names (comma separated): ").split(",")

    target = input("Enter target class column name: ")

    n = int(input("Enter number of records: "))
    dataset = []

    print("\nEnter data as comma-separated values")
    print("Format:")
    print(",".join(attributes) + "," + target)

    for i in range(n):
        row = {}
        values = input(f"Row {i + 1}: ").split(",")

        for j, attr in enumerate(attributes):
            row[attr.strip()] = values[j].strip()

        row[target] = values[-1].strip()
        dataset.append(row)

    print("\nDATASET:")
    for row in dataset:
        print(row)
    print("\nTOTAL NUMBER OF RECORDS:", len(dataset))

    # -------- ROOT NODE IDENTIFICATION --------
    print("\nFINDING ROOT NODE:")
    root_gains = {}
    for attr in attributes:
        root_gains[attr] = gain(dataset, attr, target, criterion)

    root_node = max(root_gains, key=root_gains.get)
    print(f"\nROOT NODE OF THE DECISION TREE: {root_node}")
    # -----------------------------------------

    tree = build_tree(dataset, attributes, target, criterion)

    print("\nFINAL DECISION TREE:")
    print_tree(tree)

    print("\nEnter test tuple (comma separated):")
    test_values = input(",".join(attributes) + ": ").split(",")

    sample = {}
    for i, attr in enumerate(attributes):
        sample[attr.strip()] = test_values[i].strip()

    result = predict(tree, sample)
    print("\nPredicted Target Class:", result)


# ----------------------------------------------------------
# CSV Mode (sklearn)
# ----------------------------------------------------------

def csv_mode(criterion):
    path = input("Enter CSV file path: ")
    target = input("Enter target column name: ")

    df = pd.read_csv(path)

    X = df.drop(columns=[target])
    y = df[target]

    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = LabelEncoder().fit_transform(X[col])

    if y.dtype == 'object':
        y = LabelEncoder().fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = DecisionTreeClassifier(criterion=criterion)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nTOTAL NUMBER OF RECORDS:", len(df))
    print("\nMODEL PERFORMANCE:")
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, average='weighted'))
    print("Recall   :", recall_score(y_test, y_pred, average='weighted'))
    print("F1 Score :", f1_score(y_test, y_pred, average='weighted'))


# ----------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------

def main():
    while True:
        print("\n===== DECISION TREE MENU =====")
        print("1. Build Decision Tree using Manual Data Input")
        print("2. Build Decision Tree using CSV File")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == '3':
            print("Exiting...")
            break

        print("\nChoose Splitting Criterion:")
        print("1. Entropy (Information Gain)")
        print("2. Gini Index")
        c = input("Enter choice: ")

        criterion = "entropy" if c == '1' else "gini"

        if choice == '1':
            manual_mode(criterion)
        elif choice == '2':
            csv_mode(criterion)
        else:
            print("Invalid choice!")


# ----------------------------------------------------------
# PROGRAM START
# ----------------------------------------------------------

if __name__ == "__main__":
    main()
