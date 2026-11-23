import random
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    """ Get user input for sensor type, number of readings, minimum value, maximum value, and alert threshold.
        Returns a tuple containing the sensor type, number of readings, minimum value, maximum value, and alert threshold.
    """
    
    try:
        sensor_type = input("Enter sensor type (e.g., temperatuur, vochtigheid): ").strip()
        if sensor_type.lower() in ("q", "quit"):
            print("Input cancelled.")
            return None

        number_of_readings_input = input("Enter number of readings: ").strip()
        if number_of_readings_input.lower() in ("q", "quit"):
            print("Input cancelled.")
            return None

        min_value_input = input("Enter minimum value: ").strip()
        if min_value_input.lower() in ("q", "quit"):
            print("Input cancelled.")
            return None

        max_value_input = input("Enter maximum value: ").strip()
        if max_value_input.lower() in ("q", "quit"):
            print("Input cancelled.")
            return None

        alert_threshold_input = input("Enter alert threshold: ").strip()
        if alert_threshold_input.lower() in ("q", "quit"):
            print("Input cancelled.")
            return None

        number_of_readings = int(number_of_readings_input)
        min_value = float(min_value_input)
        max_value = float(max_value_input)
        alert_threshold = float(alert_threshold_input)
    except ValueError:
        print("Error: number of readings, minimum, maximum and alert threshold must be numeric.")
        return None
    except (EOFError, KeyboardInterrupt):
        print("Error: input was cancelled.")
        return None

    if not sensor_type or not sensor_type.isalpha():
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

    numeric_values = (number_of_readings, min_value, max_value, alert_threshold)
    if not all(math.isfinite(float(value)) for value in numeric_values):
        print("Error: numeric values must be finite.")
        return None

    return sensor_type, number_of_readings, min_value, max_value, alert_threshold

def generate_sensor_data(number_of_readings, min_value, max_value):
    """ Generate random sensor data based on the number of readings, minimum value, and maximum value.
        Returns a list of random sensor readings.
    """
    if number_of_readings <= 0:
        print("Error: number of readings must be greater than 0.")
        return []
    if min_value >= max_value:
        print("Error: minimum value must be less than maximum value.")
        return []

    random.seed(42)  # Set seed for reproducibility
    readings = [round(random.uniform(min_value, max_value), 2) for _ in range(number_of_readings)]
    return readings

def save_to_csv(sensor_type, number_of_readings, readings, statistics=None,
                min_value=None, max_value=None, alert_threshold=None):
    """ Save sensor data to a CSV file.
        The CSV file is named based on the sensor type and contains the sensor readings.
    """
    if not readings:
        print("Error: no readings available to save.")
        return False

    try:
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
            writer.writerow(["Sample number:", "Reading"])
            for sample_number, reading in enumerate(readings, start=1):
                writer.writerow([sample_number, reading])
            if statistics is not None:
                writer.writerow([])
                writer.writerow(["Statistics"])
                writer.writerow(["Mean:", statistics["mean"]])
                writer.writerow(["Median:", statistics["median"]])
                writer.writerow(["Standard deviation:", statistics["std_dev"]])
                writer.writerow(["Minimum reading:", statistics["min_value"]])
                writer.writerow(["Maximum reading:", statistics["max_value"]])
                writer.writerow(["Readings above threshold:", statistics["above_threshold_count"]])
        return True
    except (OSError, csv.Error) as error:
        print(f"Error: could not save CSV file: {error}")
        return False

def plot_sensor_data(sensor_type, readings, min_value, max_value, alert_threshold):
    """ Plots a line graph of the sensor data using matplotlib.
        Saves the plot as a PNG file named based on the sensor type.
    """
    if not readings:
        print("Error: no readings available to plot.")
        return False

    try:
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
        fig.savefig(f"{sensor_type}_plot.png")
        plt.close(fig)
        return True
    except (OSError, ValueError) as error:
        print(f"Error: could not save sensor plot: {error}")
        plt.close("all")
        return False

def plot_histogram(sensor_type, readings):
    """ Plot a histogram of the sensor data using matplotlib.
        Saves the histogram as a PNG file named based on the sensor type.
    """
    if not readings:
        print("Error: no readings available to plot.")
        return False

    try:
        n_bins = 'auto'
        fig, ax = plt.subplots()
        ax.hist(readings, bins=n_bins, color='blue', edgecolor='black', alpha=0.7)
        ax.set_xlabel(f'{sensor_type} readings')
        ax.set_ylabel('Amount of readings')
        ax.set_title(f'Histogram of Sensor Data: {sensor_type}')
        fig.savefig(f"{sensor_type}_histogram.png")
        plt.close(fig)
        return True
    except (OSError, ValueError) as error:
        print(f"Error: could not save histogram: {error}")
        plt.close("all")
        return False

def load_sensor_data_from_csv(sensor_type):
    """ Load sensor data from a CSV file.
        Returns a list of sensor readings.
    """
    readings = []
    settings = {
        "number_of_readings": 0,
        "min_value": None,
        "max_value": None,
        "alert_threshold": None,
    }
    if not sensor_type or not sensor_type.isalpha():
        print("Error: sensor type must contain letters only.")
        return readings

    try:
        with open(f"{sensor_type}.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            readings_header_found = False
            for row in reader:
                if row and row[0] == "Aantal readings:":
                    try:
                        settings["number_of_readings"] = int(row[1])
                    except (IndexError, ValueError):
                        pass
                if row and row[0] == "Min value:":
                    try:
                        settings["min_value"] = float(row[1])
                    except (IndexError, ValueError):
                        pass
                if row and row[0] == "Max value:":
                    try:
                        settings["max_value"] = float(row[1])
                    except (IndexError, ValueError):
                        pass
                if row and row[0] == "Alert threshold:":
                    try:
                        settings["alert_threshold"] = float(row[1])
                    except (IndexError, ValueError):
                        pass
                if row and row[0] == "Readings":
                    readings_header_found = True
                    continue
                if readings_header_found and row:
                    try:
                        if row[0] == "Sample number:":
                            continue
                        reading_text = row[1] if len(row) > 1 and row[0].isdigit() else row[0]
                        reading = float(reading_text)
                        if math.isfinite(reading):
                            readings.append(reading)
                    except ValueError:
                        continue
            
    except FileNotFoundError:
        print(f"Error: file {sensor_type}.csv not found.")
    except (OSError, csv.Error) as error:
        print(f"Error: could not read CSV file: {error}")

    if not readings:
        print(f"Error: no valid readings found in {sensor_type}.csv.")
    return readings

def get_csv_settings(sensor_type):
    """Read the stored settings and number of readings from a sensor CSV file."""
    settings = {
        "number_of_readings": 0,
        "min_value": None,
        "max_value": None,
        "alert_threshold": None,
    }
    try:
        with open(f"{sensor_type}.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    continue
                try:
                    if row[0] == "Aantal readings:":
                        settings["number_of_readings"] = int(row[1])
                    elif row[0] == "Min value:":
                        settings["min_value"] = float(row[1])
                    elif row[0] == "Max value:":
                        settings["max_value"] = float(row[1])
                    elif row[0] == "Alert threshold:":
                        settings["alert_threshold"] = float(row[1])
                except ValueError:
                    continue
    except (OSError, csv.Error) as error:
        print(f"Error: could not read CSV settings: {error}")
    return settings

def calculate_statistics(sensor_type, readings, alert_threshold=None):
    """ Calculate statistics of the sensor data.
        Statistics include mean, median, standard deviation, minimum, and maximum values.
    """
    number_of_readings = len(readings)
    if number_of_readings == 0:
        print("No readings available to calculate statistics.")
        return None
    if any(not math.isfinite(float(reading)) for reading in readings):
        print("Error: readings must contain finite numeric values.")
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

    return {
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "min_value": min_value,
        "max_value": max_value,
        "above_threshold_count": above_threshold_count,
    }

def main():
    try:
        mode = input("Choose [old] load existing CSV or [new] generate data: ").strip().lower()
        if mode in ("q", "quit"):
            print("Input cancelled.")
            return
    except (EOFError, KeyboardInterrupt):
        print("Error: input was cancelled.")
        return

    if mode in ("old", "load", "l"):
        try:
            sensor_type = input("Enter sensor type to load: ").strip()
            if sensor_type.lower() in ("q", "quit"):
                print("Input cancelled.")
                return
        except (EOFError, KeyboardInterrupt):
            print("Error: input was cancelled.")
            return

        readings = load_sensor_data_from_csv(sensor_type)
        settings = get_csv_settings(sensor_type)
        if not readings:
            return

        number_of_readings = settings["number_of_readings"] or len(readings)
        min_value = settings["min_value"]
        max_value = settings["max_value"]
        alert_threshold = settings["alert_threshold"]

    elif mode in ("new", "generate", "n"):
        sensor_input = get_user_input()
        if sensor_input is None:
            return

        sensor_type, number_of_readings, min_value, max_value, alert_threshold = sensor_input
        readings = generate_sensor_data(number_of_readings, min_value, max_value)
    else:
        print("Error: choose 'old' or 'new'.")
        return

    if not readings:
        return

    statistics = calculate_statistics(sensor_type, readings, alert_threshold)
    if statistics is None:
        return

    if mode in ("new", "generate", "n"):
        csv_saved = save_to_csv(
            sensor_type,
            number_of_readings,
            readings,
            statistics,
            min_value,
            max_value,
            alert_threshold,
        )
    else:
        csv_saved = True

    if min_value is not None and max_value is not None and alert_threshold is not None:
        line_plot_saved = plot_sensor_data(sensor_type, readings, min_value, max_value, alert_threshold)
        histogram_saved = plot_histogram(sensor_type, readings)
    else:
        print("Error: stored min, max or alert threshold values are missing.")
        line_plot_saved = False
        histogram_saved = plot_histogram(sensor_type, readings)

    if csv_saved and line_plot_saved and histogram_saved:
        print(f"Data processed successfully for sensor type: {sensor_type}")

if __name__ == "__main__":
    main()