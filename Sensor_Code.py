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

def save_to_csv(Sensor_type, Readings, Min_value=None, Max_value=None, Alert_threshold=None):
    """ Save sensor data to a CSV file.
        The CSV file is named based on the sensor type and contains the sensor readings.
    """
    with open(f"{Sensor_type}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([f"Sensor: {Sensor_type}"])
        writer.writerow(["Readings", "Min_value", "Max_value", "Alert_threshold"])
        if Min_value is not None or Max_value is not None or Alert_threshold is not None:
            writer.writerow(["", Min_value, Max_value, Alert_threshold])
        for reading in Readings:
            writer.writerow([reading])

def plot_sensor_data(Sensor_type, Readings, Min_value, Max_value, Alert_threshold):
    """ Plots a line graph of the sensor data using matplotlib.
        Saves the plot as a PNG file named based on the sensor type.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Readings, marker='o', linestyle='-', color='b')
    ax.axhline(y=Min_value, color='r', linestyle='--', label=f'Min: {Min_value}')
    ax.axhline(y=Max_value, color='g', linestyle='--', label=f'Max: {Max_value}')
    ax.axhline(y=Alert_threshold, color='orange', linestyle='--', label=f'Alert: {Alert_threshold}')
    ax.set_xlabel('Reading Number')
    ax.set_ylabel('Value')
    ax.set_title(f'Sensor Data: {Sensor_type}')
    
    ax.grid()
    ax.legend()
    fig.savefig(f"{Sensor_type}_plot.png")  # Save the plot as a PNG file
    
    plt.close(fig)

def plot_histogram(Sensor_type, Readings):
    """ Plot a histogram of the sensor data using matplotlib.
        Saves the histogram as a PNG file named based on the sensor type.
    """
    n_bins = 'auto'  # Number of bins for the histogram
    fig, ax = plt.subplots()
    ax.hist(Readings, bins=n_bins, color='blue', edgecolor='black', alpha=0.7)
    ax.set_xlabel(f'{Sensor_type} readings')
    ax.set_ylabel('Amount of readings')
    ax.set_title(f'Histogram of Sensor Data: {Sensor_type}')
    fig.savefig(f"{Sensor_type}_histogram.png")  # Save the histogram as a PNG file
    plt.close(fig)

def load_sensor_data_from_csv(Sensor_type):
    """ Load sensor data from a CSV file.
        Returns a list of sensor readings.
    """
    Readings = []
    try:
        with open(f"{Sensor_type}.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            next(reader)
            for row in reader:
                if row:  # Check if the row is not empty
                    try:
                        Readings.append(float(row[0]))
                    except ValueError:
                        continue
            
    except FileNotFoundError:
        print(f"File {Sensor_type}.csv not found.")
    return Readings

def calculate_statistics(Sensor_type, Readings, Alert_threshold=None):
    """ Calculate statistics of the sensor data.
        Statistics include mean, median, standard deviation, minimum, and maximum values.
    """
    number_of_readings = len(Readings)
    if number_of_readings == 0:
        print("No readings available to calculate statistics.")
        return None

    mean = sum(Readings) / number_of_readings
    sorted_readings = sorted(Readings)
    if number_of_readings % 2 == 1:
        median = sorted_readings[number_of_readings // 2]
    else:
        median = (sorted_readings[number_of_readings // 2 - 1] + sorted_readings[number_of_readings // 2]) / 2

    std_dev = (sum((x - mean) ** 2 for x in Readings) / number_of_readings) ** 0.5
    min_value = np.min(Readings)
    max_value = np.max(Readings)
    if Alert_threshold is None:
        above_threshold_count = 0
    else:
        above_threshold_count = sum(1 for x in Readings if x > Alert_threshold)

    print(f"Statistics for {Sensor_type}:")
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Standard Deviation: {std_dev}")
    print(f"Minimum: {min_value}")
    print(f"Maximum: {max_value}")
    print(f"Readings above threshold: {above_threshold_count}")

if __name__ == "__main__":
    sensor_input = get_user_input()
    if sensor_input is not None:
        Sensor_type, Number_of_readings, Min_value, Max_value, Alert_threshold = sensor_input
        Readings = generate_sensor_data(Number_of_readings, Min_value, Max_value)
        save_to_csv(Sensor_type, Readings, Min_value, Max_value, Alert_threshold)
        plot_sensor_data(Sensor_type, Readings, Min_value, Max_value, Alert_threshold)
        plot_histogram(Sensor_type, Readings)
        calculate_statistics(Sensor_type, Readings, Alert_threshold)
        print(f"CSV and plots saved for sensor type: {Sensor_type}")
