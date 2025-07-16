import pandas as pd
import plotly.express as px

def plot_pitstop_counts(laps, drivers):
    import pandas as pd
    import plotly.express as px

    laps = laps[laps['Compound'].notna()].copy()
    if laps.empty or not drivers:
        return px.bar(title="无进站数据")
    laps['Stint'] = laps.groupby('Driver')['Compound'].transform(lambda x: (x != x.shift()).cumsum())

    data = []
    for drv in drivers:
        drv_stints = laps[laps['Driver'] == drv]['Stint'].nunique()
        pitstop_count = max(0, drv_stints - 1)
        data.append({'Driver': drv, 'Pitstops': pitstop_count})

    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x='Driver',
        y='Pitstops',
        title='进站次数统计图',
        text='Pitstops',
        color='Driver'
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    return fig
