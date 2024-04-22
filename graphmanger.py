import datetime
import csv
import matplotlib.pyplot as plt

class GraphManager:
    def __init__(self, file_name):
        self.dates = []
        self.hours_asleep = []
        self.alcohol_consumption = []

        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                if row[0]:
                    date = datetime.datetime.strptime(row[0], "%d/%m/%Y %H:%M")
                    self.dates.append(date)

                sleep_analysis_asleep = float(row[3]) if row[3] else 0.0
                self.hours_asleep.append(sleep_analysis_asleep)

                alcohol = float(row[1]) if row[1] else 0.0
                self.alcohol_consumption.append(alcohol)

    def plot_graphs(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        ax1.bar(self.dates, self.hours_asleep, color='blue')
        ax1.set_title("Hours Asleep Over Time")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Hours Asleep")
        ax1.set_xticks(self.dates)
        ax1.set_xticklabels([date.strftime("%Y-%m-%d") for date in self.dates], rotation=90)
        ax1.grid(axis='y')

        ax2.scatter(self.hours_asleep, self.alcohol_consumption, alpha=0.7, color='b')
        ax2.set_title("Alcohol Consumption vs. Hours Asleep")
        ax2.set_xlabel("Hours Asleep")
        ax2.set_ylabel("Alcohol Consumption (count)")
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

manager = GraphManager("test.csv")
manager.plot_graphs()
