import random
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    """ Get user input for sensor type, number of readings, minimum value, maximum value, and alert threshold.
        Returns a tuple containing the sensor type, number of readings, minimum value, maximum value, and alert threshold.
    """
    
    Sensor_type = input("Enter sensor type (e.g., temperatuur, vochtigheid): ").strip()
    Number_of_readings = int(input("Enter number of readings: "))
    Min_value = float(input("Enter minimum value: "))
    Max_value = float(input("Enter maximum value: "))
    Alert_threshold = float(input("Enter alert threshold: "))

    if not Sensor_type.isalpha():
        print("Sensor type must contain letters only.")
        return None
    
    elif Number_of_readings <= 0:
        print("Number of readings must be greater than 0.")
        return None
    
    elif Min_value >= Max_value:
        print("Minimum value must be less than maximum value.")
        return None

    elif Alert_threshold < Min_value or Alert_threshold > Max_value:
        print("Alert threshold must be between minimum and maximum values.")
        return None

    return Sensor_type, Number_of_readings, Min_value, Max_value, Alert_threshold

def generate_sensor_data(Numer_of_readings, Min_value, Max_value):
    """ Generate random sensor data based on the number of readings, minimum value, and maximum value.
        Returns a list of random sensor readings.
    """
    random.seed(42)  # Set seed for reproducibility
    Readings = [round(random.uniform(Min_value, Max_value), 2) for _ in range(Numer_of_readings)]
    return Readings

def save_to_csv(Sensor_type, Readings):
    """ Save sensor data to a CSV file.
        The CSV file is named based on the sensor type and contains the sensor readings.
    """
    with open(f"{Sensor_type}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([f"Sensor: {Sensor_type}"])
        writer.writerow(["Readings", "Min_value", "Max_value", "Alert_threshold"])
        for reading in Readings:
            writer.writerow([reading])

def plot_sensor_data(Sensor_type, Readings, Min_value, Max_value, Alert_threshold):
    """ Plot sensor data using matplotlib.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(Readings, marker='o', linestyle='-', color='b')
    plt.axhline(y=Min_value, color='r', linestyle='--', label=f'Min: {Min_value}')
    plt.axhline(y=Max_value, color='g', linestyle='--', label=f'Max: {Max_value}')
    plt.axhline(y=Alert_threshold, color='orange', linestyle='--', label=f'Alert: {Alert_threshold}')
    plt.xlabel('Reading Number')
    plt.ylabel('Value')
    plt.title(f'Sensor Data: {Sensor_type}')
    plt.legend()
    plt.show()

def plot_histogram(Sensor_type, Readings):
    """ Plot a histogram of the sensor data using matplotlib.
    """
    plt.figure(figsize=(10, 5))
    plt.hist(Readings, bins=10, color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Sensor Data: {Sensor_type}')
    plt.show()

if __name__ == "__main__":
    sensor_input = get_user_input()
    print(sensor_input)
