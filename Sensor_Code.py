import random
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    Sensor_type = input("Enter sensor type (e.g., temperatuur, vochtigheid): ")
    Number_of_readings = int(input("Enter number of readings: "))
    Min_value = float(input("Enter minimum value: "))
    Max_value = float(input("Enter maximum value: "))
    Alert_threshold = float(input("Enter alert threshold: "))

    if Number_of_readings <= 0:
        raise ValueError("Number of readings must be greater than 0.")
        return None
    
    elif Min_value >= Max_value:
        raise ValueError("Minimum value must be less than maximum value.")
        return None

    elif Alert_threshold < Min_value or Alert_threshold > Max_value:
        raise ValueError("Alert threshold must be between minimum and maximum values.")
        return None

    return Sensor_type, Number_of_readings, Min_value, Max_value, Alert_threshold
