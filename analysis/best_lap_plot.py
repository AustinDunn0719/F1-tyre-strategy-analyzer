import pandas as pd
import plotly.express as px

def plot_best_laps(session, drivers):
    import pandas as pd
    import plotly.express as px

    if not hasattr(session, "laps") or session.laps.empty:
        return px.bar(title="无圈速数据")
    if not drivers:
        return px.bar(title="未选择车手")

    data = []
    for drv in drivers:
        laps = session.laps.pick_drivers([drv]).pick_accurate().copy()
        if 'LapTime' not in laps or laps['LapTime'].isna().all():
            continue
        if not pd.api.types.is_timedelta64_dtype(laps['LapTime']):
            continue
        laps = laps[laps['LapTime'].notna()]
        if not laps.empty:
            best = laps['LapTime'].min().total_seconds()
            data.append({'Driver': drv, 'BestLapTime': best})

    if not data:
        return px.bar(title="无有效圈速数据")
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x='Driver',
        y='BestLapTime',
        title='最佳圈速对比图（秒）',
        text='BestLapTime',
        color='Driver'
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    return fig
