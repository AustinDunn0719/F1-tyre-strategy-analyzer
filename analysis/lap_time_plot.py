import matplotlib.pyplot as plt
import seaborn as sns

def plot_lap_times(session, drivers):
    plt.figure(figsize=(10, 5))
    for driver in drivers:
        laps = session.laps.pick_driver(driver).pick_accurate()
        lap_times = laps['LapTime'].dt.total_seconds()
        sns.lineplot(x=laps['LapNumber'], y=lap_times, label=driver)
    plt.xlabel('Lap')
    plt.ylabel('Lap Time (s)')
    plt.title(f"Lap Time Comparison - {session.event['EventName']}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
