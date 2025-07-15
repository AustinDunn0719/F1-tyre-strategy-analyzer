import os
import fastf1
from analysis.lap_time_plot import plot_lap_times
from analysis.tyre_strategy_plot import plot_tyre_strategy

# 初始化缓存目录,如果 cache/ 目录不存在，就创建它（用于缓存下载的数据文件，避免重复访问）
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')

# 设置比赛：年、编号、Session 类型
session = fastf1.get_session(2023, 5, 'R')  # 摩纳哥 2023 第5场 正赛
session.load()

# 分析车手
drivers = ['VER', 'ALO']

# 圈速趋势图
plot_lap_times(session, drivers)

# 用胎策略图,它会绘制该车手的轮胎使用条形图，展示每一段 stint 使用的是哪种轮胎、持续多少圈
for driver in drivers:
    plot_tyre_strategy(session.laps, driver)
