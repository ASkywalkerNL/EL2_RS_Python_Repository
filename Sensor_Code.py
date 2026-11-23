import random
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
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
