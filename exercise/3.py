import math
import pandas as pd
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from pathlib import Path

# --- Distance Functions ---
def euclidean_distance(p1, p2):
    return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(p1, p2)))

def manhattan_distance(p1, p2):
    return sum(abs(float(a) - float(b)) for a, b in zip(p1, p2))

def chebyshev_distance(p1, p2):
    return max(abs(float(a) - float(b)) for a, b in zip(p1, p2))

def get_k_value(n_train):
    k = max(1, int(n_train * 0.10))
    if k % 2 == 0: k += 1
    return k

# --- Core KNN Logic ---
def calculate_votes(neighbors, weighted=False):
    if not weighted:
        labels = [n[1] for n in neighbors]
        return Counter(labels).most_common(1)[0][0]
    else:
        weights = {}
        for dist, label in neighbors:
            w = 1 / dist if dist != 0 else 1e10
            weights[label] = weights.get(label, 0) + w
        return max(weights, key=weights.get)

def perform_knn(train_data, train_labels, query_point, k, dist_metric_choice, vote_choice):
    distances = []
    for i in range(len(train_data)):
        if dist_metric_choice == '1':
            d = euclidean_distance(query_point, train_data[i])
        elif dist_metric_choice == '2':
            d = manhattan_distance(query_point, train_data[i])
        else:
            d = chebyshev_distance(query_point, train_data[i])
        distances.append((d, train_labels[i]))

    # Sort by distance to establish rank
    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    prediction = calculate_votes(neighbors, weighted=(vote_choice == '2'))
    # Return both the prediction and the ranked neighbors for logging
    return prediction, neighbors

# --- Evaluation ---
def evaluate_model(true_labels, predicted_labels):
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    print(f"\n[Evaluation Metrics]")
    print(f"Accuracy: {accuracy:.2f} | Precision: {precision:.2f} | Recall: {recall:.2f} | F1 Score: {f1:.2f}")

    print("\n[Confusion Matrix]")
    unique_labels = sorted(list(set(true_labels) | set(predicted_labels)))
    cm = confusion_matrix(true_labels, predicted_labels, labels=unique_labels)
    cm_df = pd.DataFrame(cm, index=unique_labels, columns=unique_labels)
    print(cm_df)

# --- Main Program ---
def main():
    print("--- KNN Classifier ---")
    print("1. Manual Input | 2. CSV File Input")
    choice = input("Select option: ")

    train_data, train_labels, test_data, test_labels = [], [], [], []

    if choice == '1':
        num_feats = int(input("Enter number of features: "))
        num_points = int(input("Enter number of training data points: "))

        for i in range(num_points):
            row = [float(x) for x in input(f"Features for point {i+1} (space separated): ").split()]
            lbl = input(f"Label for point {i+1}: ")
            train_data.append(row)
            train_labels.append(lbl)

        query = [float(x) for x in input("\nEnter features for test point: ").split()]
        actual_lbl = input("Enter actual label for this test point: ")
        test_data = [query]
        test_labels = [actual_lbl]
        k_val = int(input("Enter K value: "))

    elif choice == '2':
        filename = input("Enter CSV filename: ")
        path = Path("//172.16.16.220/cse-student/UG/23BCS/A/19522/sem6/ci/ex3")/filename

        if not path.exists():
            print(f"Error: File not found at {path}")
            return

        df = pd.read_csv(path)
        col_indices = [int(x) for x in input("\nEnter feature column indices (comma separated): ").split(',')]
        label_index = int(input("Enter label column index: "))
        test_size = float(input("Enter % of test data: ")) / 100

        tr_df, ts_df = train_test_split(df, test_size=test_size, random_state=42)

        train_data = tr_df.iloc[:, col_indices].values.tolist()
        train_labels = tr_df.iloc[:, label_index].values.tolist()
        test_data = ts_df.iloc[:, col_indices].values.tolist()
        test_labels = ts_df.iloc[:, label_index].values.tolist()
        k_val = get_k_value(len(train_data))
        print(f"Using K = {k_val}")

    else:
        print("Invalid choice.")
        return

    dist_c = input("Distance: 1. Euclidean | 2. Manhattan | 3. Chebyshev: ")
    vote_c = input("Voting: 1. Unweighted | 2. Weighted: ")

    # Process predictions and capture neighbor data
    all_results = [perform_knn(train_data, train_labels, row, k_val, dist_c, vote_c) for row in test_data]
    predictions = [res[0] for res in all_results]

    # --- Print Ranking for the first test point ---
    print("\n--- Neighbor Ranking (First Test Point) ---")
    print(f"{'Rank':<6} | {'Distance':<12} | {'Label':<10}")
    print("-" * 35)
    first_point_neighbors = all_results[0][1]
    for rank, (dist, label) in enumerate(first_point_neighbors, 1):
        print(f"{rank:<6} | {dist:<12.4f} | {label:<10}")

    print(f"\n[Result] Predicted: {predictions[0]} | Actual: {test_labels[0]}")
    evaluate_model(test_labels, predictions)

if __name__ == "__main__":
    main()
