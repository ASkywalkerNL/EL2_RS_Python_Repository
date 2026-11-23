import random
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    """ Get user input for sensor type, number of readings, minimum value, maximum value, and alert threshold.
        Returns a tuple containing the sensor type, number of readings, minimum value, maximum value, and alert threshold.
    """
    
    sensor_type = input("Enter sensor type (e.g., temperatuur, vochtigheid): ").strip()
    number_of_readings = int(input("Enter number of readings: "))
    min_value = float(input("Enter minimum value: "))
    max_value = float(input("Enter maximum value: "))
    alert_threshold = float(input("Enter alert threshold: "))

    if not sensor_type.isalpha():
        print("Sensor type must contain letters only.")
        return None
    
    elif number_of_readings <= 0:
        print("Number of readings must be greater than 0.")
        return None
    
    elif min_value >= max_value:
        print("Minimum value must be less than maximum value.")
        return None

    elif alert_threshold < min_value or alert_threshold > max_value:
        print("Alert threshold must be between minimum and maximum values.")
        return None

    return sensor_type, number_of_readings, min_value, max_value, alert_threshold

def generate_sensor_data(number_of_readings, min_value, max_value):
    """ Generate random sensor data based on the number of readings, minimum value, and maximum value.
        Returns a list of random sensor readings.
    """
    random.seed(42)  # Set seed for reproducibility
    readings = [round(random.uniform(min_value, max_value), 2) for _ in range(number_of_readings)]
    return readings

def save_to_csv(sensor_type, number_of_readings, readings, min_value=None, max_value=None, alert_threshold=None):
    """ Save sensor data to a CSV file.
        The CSV file is named based on the sensor type and contains the sensor readings.
    """
    with open(f"{sensor_type}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([f"Sensor type:", sensor_type])
        writer.writerow([])
        writer.writerow(["Aantal readings:", number_of_readings])
        writer.writerow(["Min value:", min_value])
        writer.writerow(["Max value:", max_value])
        writer.writerow(["Alert threshold:", alert_threshold])
        writer.writerow([])
        writer.writerow(["Readings"])
        for reading in readings:
            writer.writerow([reading])

def plot_sensor_data(sensor_type, readings, min_value, max_value, alert_threshold):
    """ Plots a line graph of the sensor data using matplotlib.
        Saves the plot as a PNG file named based on the sensor type.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(readings, marker='o', linestyle='-', color='b')
    ax.axhline(y=min_value, color='r', linestyle='--', label=f'Min: {min_value}')
    ax.axhline(y=max_value, color='g', linestyle='--', label=f'Max: {max_value}')
    ax.axhline(y=alert_threshold, color='orange', linestyle='--', label=f'Alert: {alert_threshold}')
    ax.set_xlabel('Reading Number')
    ax.set_ylabel('Value')
    ax.set_title(f'Sensor Data: {sensor_type}')
    
    ax.grid()
    ax.legend()
    fig.savefig(f"{sensor_type}_plot.png")  # Save the plot as a PNG file
    
    plt.close(fig)

def plot_histogram(sensor_type, readings):
    """ Plot a histogram of the sensor data using matplotlib.
        Saves the histogram as a PNG file named based on the sensor type.
    """
    n_bins = 'auto'  # Number of bins for the histogram
    fig, ax = plt.subplots()
    ax.hist(readings, bins=n_bins, color='blue', edgecolor='black', alpha=0.7)
    ax.set_xlabel(f'{sensor_type} readings')
    ax.set_ylabel('Amount of readings')
    ax.set_title(f'Histogram of Sensor Data: {sensor_type}')
    fig.savefig(f"{sensor_type}_histogram.png")  # Save the histogram as a PNG file
    plt.close(fig)

def load_sensor_data_from_csv(sensor_type):
    """ Load sensor data from a CSV file.
        Returns a list of sensor readings.
    """
    readings = []
    try:
        with open(f"{sensor_type}.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            readings_header_found = False
            for row in reader:
                if row and row[0] == "Readings":
                    readings_header_found = True
                    continue
                if readings_header_found and row:
                    try:
                        readings.append(float(row[0]))
                    except ValueError:
                        continue
            
    except FileNotFoundError:
        print(f"File {sensor_type}.csv not found.")
    return readings

def calculate_statistics(sensor_type, readings, alert_threshold=None):
    """ Calculate statistics of the sensor data.
        Statistics include mean, median, standard deviation, minimum, and maximum values.
    """
    number_of_readings = len(readings)
    if number_of_readings == 0:
        print("No readings available to calculate statistics.")
        return None

    mean = sum(readings) / number_of_readings
    sorted_readings = sorted(readings)
    if number_of_readings % 2 == 1:
        median = sorted_readings[number_of_readings // 2]
    else:
        median = (sorted_readings[number_of_readings // 2 - 1] + sorted_readings[number_of_readings // 2]) / 2

    std_dev = (sum((x - mean) ** 2 for x in readings) / number_of_readings) ** 0.5
    min_value = np.min(readings)
    max_value = np.max(readings)
    if alert_threshold is None:
        above_threshold_count = 0
    else:
        above_threshold_count = sum(1 for x in readings if x > alert_threshold)

    print(f"Statistics for {sensor_type}:")
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Standard Deviation: {std_dev}")
    print(f"Minimum: {min_value}")
    print(f"Maximum: {max_value}")
    print(f"Readings above threshold: {above_threshold_count}")

def main():
    sensor_input = get_user_input()
    if sensor_input is not None:
        sensor_type, number_of_readings, min_value, max_value, alert_threshold = sensor_input
        readings = generate_sensor_data(number_of_readings, min_value, max_value)
        save_to_csv(sensor_type, number_of_readings, readings, min_value, max_value, alert_threshold)
        plot_sensor_data(sensor_type, readings, min_value, max_value, alert_threshold)
        plot_histogram(sensor_type, readings)
        calculate_statistics(sensor_type, readings, alert_threshold)
        print(f"CSV and plots saved for sensor type: {sensor_type}")

if __name__ == "__main__":
    main()