import pandas as pd
import plotly.express as px

def plot_lap_times(session, drivers):
    import pandas as pd
    import plotly.express as px

    if not hasattr(session, "laps") or session.laps.empty:
        return px.line(title="无圈速数据")
    if not drivers:
        return px.line(title="未选择车手")

    fig = None
    all_laps = []

    for drv in drivers:
        laps = session.laps.pick_drivers([drv]).pick_accurate().copy()
        if 'LapTime' not in laps or laps['LapTime'].isna().all():
            continue
        if not pd.api.types.is_timedelta64_dtype(laps['LapTime']):
            continue
        laps.loc[:, 'LapTime(s)'] = laps['LapTime'].dt.total_seconds()
        laps.loc[:, 'Driver'] = drv
        all_laps.append(laps[['LapNumber', 'LapTime(s)', 'Driver']])

    if not all_laps:
        return px.line(title="无有效圈速数据")
    df = pd.concat(all_laps)
    fig = px.line(df, x="LapNumber", y="LapTime(s)", color="Driver",
                  title="圈速趋势图", markers=True)
    return fig
