import plotly.express as px
# from fastf1 import plotting

# 手动定义轮胎配色字典
COMPOUND_COLORS = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFCC33',
    'HARD': '#FFFFFF',
    'INTERMEDIATE': '#39B54A',
    'WET': '#0090FF',
    'C5': '#FF3333',
    'C4': '#FF3333',
    'C3': '#FFCC33',
    'C2': '#FFFFFF',
    'C1': '#E0E0E0',
    # 可根据实际需要补充
}

def plot_tyre_strategy(laps, driver):
    # 选中指定车手并过滤无效轮胎数据
    drv_laps = laps[laps['Driver'] == driver].copy()
    drv_laps = drv_laps[drv_laps['Compound'].notna()].copy()

    if drv_laps.empty:
        return px.bar(title=f"{driver} 无可用胎数据")

    # 识别轮胎变化点（分段）
    drv_laps.loc[:, 'Stint'] = (drv_laps['Compound'] != drv_laps['Compound'].shift()).cumsum()

    # 统计每个 Stint 的范围与轮胎类型
    stints = drv_laps.groupby('Stint').agg({
        'LapNumber': ['min', 'max'],
        'Compound': 'first'
    }).reset_index()

    # 重命名多重列
    stints.columns = ['Stint', 'LapStart', 'LapEnd', 'Compound']

    # 计算每个 stint 的长度与颜色
    stints['duration'] = stints['LapEnd'] - stints['LapStart'] + 1
    stints['CompoundColor'] = stints['Compound'].map(COMPOUND_COLORS).fillna('gray')
    stints['Driver'] = driver

    # 画图
    fig = px.bar(
        stints,
        x='duration',
        y='Driver',
        color='Compound',
        orientation='h',
        custom_data=['LapStart', 'LapEnd'],
        color_discrete_map=COMPOUND_COLORS,
        title=f"{driver} 的用胎策略"
    )

    fig.update_traces(
        hovertemplate='从第 %{customdata[0]} 圈到 %{customdata[1]} 圈<br>用胎：%{marker.color}'
    )

    return fig
