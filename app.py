import streamlit as st
import fastf1
import os
import pandas as pd
import plotly.express as px

from analysis.lap_time_plot import plot_lap_times
from analysis.tyre_strategy_plot import plot_tyre_strategy
from analysis.avg_laptime_plot import plot_avg_lap_times
from analysis.pitstop_count_plot import plot_pitstop_counts
from analysis.best_lap_plot import plot_best_laps

# 设置缓存
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')

st.title("🏎️ F1 数据分析平台")

# ==== 参数设置 ====
st.sidebar.header("参数设置")
year = st.sidebar.selectbox("年份", [2023, 2024], index=0)

# 多站比较模式
multi_mode = st.sidebar.checkbox("启用多站比较", value=False)

if multi_mode:
    selected_rounds = st.sidebar.multiselect("选择多个比赛站（最多 5 个）", list(range(1, 24)), default=[1, 5])
    driver_to_compare = st.sidebar.selectbox("选择分析车手", ['VER', 'HAM', 'LEC', 'NOR', 'SAI'])
    if st.sidebar.button("📊 加载多站数据"):
        with st.spinner("加载多个分站数据中..."):
            def load_multiple_sessions(year, rounds):
                sessions = []
                for rnd in rounds:
                    try:
                        s = fastf1.get_session(year, rnd, 'R')
                        s.load()
                        sessions.append((rnd, s))
                    except Exception as e:
                        st.warning(f"第 {rnd} 站加载失败：{e}")
                return sessions

            session_list = load_multiple_sessions(year, selected_rounds)

        if session_list:
            st.success("✅ 多站数据加载完毕")
            multi_df = []
            for rnd, session in session_list:
                laps = session.laps.pick_drivers([driver_to_compare]).pick_accurate().copy()
                laps = laps[laps['LapTime'].notna()]
                if laps.empty:
                    continue
                laps['LapTime(s)'] = laps['LapTime'].dt.total_seconds()
                laps['Round'] = f"Round {rnd}"
                multi_df.append(laps[['LapNumber', 'LapTime(s)', 'Round']])

            if multi_df:
                df = pd.concat(multi_df)
                fig = px.line(df, x="LapNumber", y="LapTime(s)", color="Round",
                              title=f"{driver_to_compare} 多站圈速趋势图", markers=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("未获取到任何圈速数据")
        else:
            st.error("所有分站加载失败，无法生成图表")
else:
    # ==== 单站分析 ====
    round_number = st.sidebar.slider("比赛站数", 1, 23, 5)
    session_type = st.sidebar.radio("Session 类型", ['FP1', 'FP2', 'FP3', 'Q', 'R'], index=4)

    if 'session_loaded' not in st.session_state:
        st.session_state.session_loaded = False
    if 'session_data' not in st.session_state:
        st.session_state.session_data = None

    if st.sidebar.button("🔄 加载比赛"):
        with st.spinner("加载中..."):
            try:
                year_val = int(year) if year is not None else 2023
                round_val = int(round_number) if round_number is not None else 5
                session_type_val = str(session_type) if session_type is not None else 'R'
                session = fastf1.get_session(year_val, round_val, session_type_val)
                session.load()
                st.session_state.session_loaded = True
                st.session_state.session_data = session
                st.success("✅ 数据加载成功！")
            except Exception as e:
                st.error(f"加载失败：{e}")

    if st.session_state.session_loaded and st.session_state.session_data is not None:
        session = st.session_state.session_data
        if hasattr(session, 'laps') and session.laps is not None and not session.laps.empty and 'Driver' in session.laps:
            available_drivers = session.laps['Driver'].unique().tolist()
            drivers = st.multiselect("选择车手", available_drivers, default=available_drivers[:2])

            if st.button("📊 生成图表"):
                try:
                    st.subheader("📈 圈速趋势图")
                    fig1 = plot_lap_times(session, drivers)
                    if fig1:
                        st.plotly_chart(fig1, use_container_width=True)
                    else:
                        st.warning("无圈速数据")

                    for drv in drivers:
                        st.subheader(f"🛞 {drv} 用胎策略")
                        fig2 = plot_tyre_strategy(session.laps, drv)
                        if fig2:
                            st.plotly_chart(fig2, use_container_width=True)
                        else:
                            st.warning(f"{drv} 无用胎数据")

                    st.subheader("📉 平均圈速对比图")
                    fig3 = plot_avg_lap_times(session, drivers)
                    if fig3:
                        st.plotly_chart(fig3, use_container_width=True)
                    else:
                        st.warning("无平均圈速数据")

                    st.subheader("🛑 进站次数统计图")
                    fig4 = plot_pitstop_counts(session.laps, drivers)
                    if fig4:
                        st.plotly_chart(fig4, use_container_width=True)
                    else:
                        st.warning("无进站数据")

                    st.subheader("🏁 最佳圈速对比图")
                    fig5 = plot_best_laps(session.laps, drivers)
                    if fig5:
                        st.plotly_chart(fig5, use_container_width=True)
                    else:
                        st.warning("无最佳圈速数据")
                except Exception as e:
                    st.error(f"生成图表时出错：{e}")
        else:
            st.warning("未能获取有效的圈速数据，无法选择车手。请检查数据源或重新加载比赛。")
