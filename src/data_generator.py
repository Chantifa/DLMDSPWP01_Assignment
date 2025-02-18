import numpy as np
import csv
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the data folder exists at the same level as src
data_dir = os.path.join(script_dir, '..', 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Training Data
for i in range(1, 5):
    with open(os.path.join(data_dir, f'training_data_{i}.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y'])
        for j in range(1, 6):
            writer.writerow([j, j * (i * 0.1 + 2)])

# Ideal Functions
with open(os.path.join(data_dir, 'ideal_functions.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    headers = ['X']
    for i in range(1, 51):
        headers.append(f'Y{i}')
    writer.writerow(headers)
    for j in range(1, 6):  # Assuming 5 data points for simplicity
        row = [j]
        for i in range(1, 51):
            row.append(j * i * 0.1)  # Simple linear function for each ideal function
        writer.writerow(row)

# Test Data
with open(os.path.join(data_dir, 'test_data.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['X', 'Y'])
    for j in np.linspace(1.5, 5.5, 5):  # 5 points between 1.5 and 5.5
        writer.writerow([j, j * 2])  # Simple linear function for test data