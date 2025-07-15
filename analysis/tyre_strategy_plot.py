import matplotlib.pyplot as plt
from fastf1 import plotting

def plot_tyre_strategy(laps, driver_code):
    driver_laps = laps.pick_driver(driver_code).pick_accurate()
    stints = driver_laps.get_stints()
    stints['colour'] = stints['Compound'].map(plotting.COMPOUND_COLORS)

    fig, ax = plt.subplots(figsize=(10, 1.5))
    for _, stint in stints.iterrows():
        ax.barh(driver_code,
                stint['LapEnd'] - stint['LapStart'] + 1,
                left=stint['LapStart'],
                color=stint['colour'])
    ax.set_xlabel('Lap')
    ax.set_title(f"{driver_code}'s Tyre Strategy")
    plt.tight_layout()
    plt.show()
