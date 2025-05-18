import csv
import matplotlib.pyplot as plt  # Correct import for plotting

# Constants
Experiment_altitude = 2072.64  # 6800 feet
Experiment_altitude_error = 1  # %
Experiment_v0 = 75  # Knots
Experiment_vf = 103

# Columns to remove from the raw data
Useless_Columns = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

class Data:
    def __init__(self):
        Raw_Data = Data.GetData(r'C:\Uni\Air transport\Project\Log2.csv')
        Raw_Data_2 = Raw_Data[2:]  # Skip header/indicator rows
        Raw_Data_3 = Data.GetData_Altitude(Raw_Data_2)
        Raw_Data_4 = Data.GetData_Without_Columns(Raw_Data_3)
        Raw_Data_5 = Data.GetData_Right_Units(Raw_Data_4)
        Raw_Data_6 = Raw_Data_5[1713:2300]

        Data_1 = Raw_Data_6[:67] #First Data Set
        Data_2 = Raw_Data_6[257:312] #Second Data Set
        Data_3 = Raw_Data_6[458:545]

        self.Data_1 = Data_1
        self.Data_2 = Data_2
        self.Data_3 = Data_3

    @staticmethod
    def GetData(filepath):
        Data = []
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                Data.append(row)
        return Data

    @staticmethod
    def GetData_Altitude(data):
        Altitude = Experiment_altitude
        Error = Experiment_altitude_error
        Range_altitude = [
            Altitude - Altitude * Error * 0.01,
            Altitude + Altitude * Error * 0.01
        ]
        Filtered_Data = []
        for row in data:
            try:
                altitude = float(row[5])
                if Range_altitude[0] < altitude < Range_altitude[1]:
                    Filtered_Data.append(row)
            except (ValueError, IndexError):
                continue
        return Filtered_Data

    @staticmethod
    def GetData_Without_Columns(data):
        for row in data:
            for column in sorted(Useless_Columns, reverse=True):
                try:
                    row.pop(column)
                except IndexError:
                    continue
        return data

    @staticmethod
    def GetData_Right_Units(data):
        for row in data:
            try:
                row[0] = float(row[0]) / 128
                row[1] = float(row[1]) * 4.448
                row[2] = (float(row[2]) * -360) / (65536 ** 2)
            except (ValueError, IndexError):
                continue
        return data
    
    

# Plot Vias (Airspeed?) vs Time
def Plot_Vias_vs_Time(data):
    x_time = list(range(len(data)))
    y_vias = [float(row[0]) for row in data if len(row) > 1]

    plt.plot(x_time, y_vias, label="Vias")
    plt.xlabel("Time (samples)")
    plt.ylabel("Vias (knots)")
    plt.title("Vias vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()

# Plot Pitch vs Time
def Plot_Pitch_vs_Time(data):
    x_time = list(range(len(data)))
    y_pitch = [float(row[2]) for row in data if len(row) > 3]

    plt.plot(x_time, y_pitch, label="Pitch")
    plt.xlabel("Time (samples)")
    plt.ylabel("Pitch (degrees)")
    plt.title("Pitch vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()

def export_data_to_csv(data_instance):
    # Export Data_1
    with open('Data_1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_instance.Data_1)
    
    # Export Data_2
    with open('Data_2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_instance.Data_2)
    
    # Export Data_3
    with open('Data_3.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_instance.Data_3)

# Main Execution
D = Data()

#Plot_Vias_vs_Time(D.Data_1)
#Plot_Vias_vs_Time(D.Data_2)
Plot_Vias_vs_Time(D.Data_3)
#Plot_Pitch_vs_Time(D.Data_1)
#Plot_Pitch_vs_Time(D.Data_1)
Plot_Pitch_vs_Time(D.Data_3)

export_data_to_csv(D)