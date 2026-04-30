import numpy as np

# ---------------- Activation Functions ----------------
def threshold(x):
    return 1 if x >= 0 else 0

def bipolar_threshold(x):
    return 1 if x >= 0 else -1

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

# ---------------- User Inputs ----------------
alpha = float(input("Enter learning rate (alpha): "))
n = int(input("Enter number of inputs: "))

weights = np.array([float(input(f"Enter initial weight w{i+1}: ")) for i in range(n)])
b = float(input("Enter bias: "))

# NEW: Get max epochs from user
max_epochs = int(input("Enter number of epochs: "))

print("\nChoose Gate:")
print("1. AND\n2. OR\n3. NAND\n4. NOR\n5. XOR\n6. XNOR\n7. NOT")
gate_choice = int(input("Enter choice: "))

print("\nChoose Activation Function:")
print("1. Threshold\n2. Sigmoid\n3. Tanh")
act_choice = int(input("Enter choice: "))

# ---------------- USER ENTERS DATASET ----------------
print("\nEnter number of training samples:")
m = int(input())

inputs = []
print("Enter inputs row by row (space separated):")
for i in range(m):
    row = list(map(int, input().split()))
    inputs.append(row)

inputs = np.array(inputs)

# ---------------- AUTO DETECT INPUT TYPE ----------------
if np.any(inputs == -1):
    type_choice = 2
else:
    type_choice = 1

print("\nDetected Input Type:", "Bipolar (-1,1)" if type_choice == 2 else "Binary (0,1)")

# ---------------- TARGET GENERATION ----------------
targets = []

for x in inputs:
    temp = np.where(x == 1, 1, 0)

    if gate_choice == 1:
        out = 1 if np.all(temp) else 0
    elif gate_choice == 2:
        out = 1 if np.any(temp) else 0
    elif gate_choice == 3:
        out = 0 if np.all(temp) else 1
    elif gate_choice == 4:
        out = 0 if np.any(temp) else 1
    elif gate_choice == 5:
        out = np.sum(temp) % 2
    elif gate_choice == 6:
        out = 0 if np.sum(temp) % 2 else 1
    elif gate_choice == 7:
        if n != 1:
            print("NOT gate requires 1 input")
            exit()
        out = 0 if temp[0] == 1 else 1

    if type_choice == 2:
        out = 1 if out == 1 else -1

    targets.append(out)

targets = np.array(targets)

# ---------------- Activation Selection ----------------
if act_choice == 1:
    act = threshold if type_choice == 1 else bipolar_threshold
elif act_choice == 2:
    act = sigmoid
elif act_choice == 3:
    act = tanh

# ---------------- Training ----------------
print("\n================ TRAINING START ================\n")

for epoch in range(max_epochs):
    print(f"\n******** EPOCH {epoch+1} ********\n")

    no_update = True

    # TABLE HEADER
    header = ["x"+str(i+1) for i in range(n)] + ["t", "yin", "y"]
    header += [f"Δw{i+1}" for i in range(n)] + ["Δb"]
    header += [f"w{i+1}" for i in range(n)] + ["b"]

    print(" ".join(h.center(6) for h in header))
    print("-" * (7 * len(header)))

    for i in range(len(inputs)):
        x = inputs[i]
        t = targets[i]

        yin = np.dot(x, weights) + b
        y = act(yin)

        if act_choice == 2:
            y = 1 if y >= 0.5 else (0 if type_choice == 1 else -1)
        elif act_choice == 3:
            y = 1 if y >= 0 else (0 if type_choice == 1 else -1)

        delta_w = np.zeros(n)
        delta_b = 0

        if y != t:
            delta_w = alpha * t * x
            delta_b = alpha * t

            weights = weights + delta_w
            b = b + delta_b
            no_update = False

        error = t - y

        row = list(x) + [t, round(yin, 2), y]
        row += list(delta_w.astype(int)) + [int(delta_b)]
        row += list(weights.astype(int)) + [int(b)]

        print(" ".join(str(val).center(6) for val in row))

    # Convergence / Epoch End Handling
    if no_update:
        print("\nConverged!")
        break
    else:
        print("\n End of Epoch", epoch+1)
        print("Updated Weights:", weights)
        print("Updated Bias:", b)

else:
    print("\nDid NOT converge")

print("\n================ TRAINING END ================\n")

# ---------------- Final Output ----------------
print("\nFinal Outputs:")
print("Inputs -> Output")
print("-"*30)

for x in inputs:
    yin = np.dot(x, weights) + b
    y = act(yin)

    if act_choice == 2:
        y = 1 if y >= 0.5 else (0 if type_choice == 1 else -1)
    elif act_choice == 3:
        y = 1 if y >= 0 else (0 if type_choice == 1 else -1)

    print(f"{tuple(x)} -> {y}")
