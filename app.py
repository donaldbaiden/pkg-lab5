from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from logic import ClipWindow, Segment, liang_barsky_clip, parse_input_data

st.set_page_config(page_title="Lab5 · Алгоритм Лианга-Барски", layout="wide")
st.title("Lab5 · Отсечение отрезков (Лианг-Барски)")

DEFAULT_INPUT = """3
-50 10 20 60
10 -20 80 40
-30 80 60 -10
0 0 50 50"""

col_setup, col_viz = st.columns([1, 2])

with col_setup:
    st.subheader("Входные данные")
    st.caption("Формат:\nN (число)\nX1 Y1 X2 Y2 (отрезки)\n...\nXmin Ymin Xmax Ymax (окно)")
    input_text = st.text_area("Данные", DEFAULT_INPUT, height=200)
    
    segments, window = parse_input_data(input_text)
    
    if not window:
        st.error("Не удалось прочитать координаты окна (последняя строка).")
    elif not segments:
        st.warning("Нет отрезков для отображения.")
    else:
        st.success(f"Загружено: {len(segments)} отрезков, окно [{window.x_min}, {window.y_min}]-[{window.x_max}, {window.y_max}]")

if window and segments:
    with col_viz:
        st.subheader("Визуализация")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        
        rect_x = [window.x_min, window.x_max, window.x_max, window.x_min, window.x_min]
        rect_y = [window.y_min, window.y_min, window.y_max, window.y_max, window.y_min]
        ax.plot(rect_x, rect_y, color='blue', linewidth=2, label='Окно отсечения')
        ax.fill(rect_x, rect_y, color='blue', alpha=0.05)
        
        visible_count = 0
        
        for i, seg in enumerate(segments):
            ax.plot([seg.p1.x, seg.p2.x], [seg.p1.y, seg.p2.y], 
                   color='gray', linestyle='--', alpha=0.5, label='Исходные' if i == 0 else "")
            
            clipped = liang_barsky_clip(seg, window)
            
            if clipped:
                visible_count += 1
                ax.plot([clipped.p1.x, clipped.p2.x], [clipped.p1.y, clipped.p2.y], 
                       color='red', linewidth=2, marker='o', markersize=4, label='Видимая часть' if visible_count == 1 else "")
        
        ax.legend(loc='upper right')
        ax.set_aspect('equal')
        
        all_x = [p for s in segments for p in (s.p1.x, s.p2.x)] + [window.x_min, window.x_max]
        all_y = [p for s in segments for p in (s.p1.y, s.p2.y)] + [window.y_min, window.y_max]
        margin = 10
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        ax.set_title(f"Результат: {visible_count} видимых (частично или полностью) из {len(segments)}")
        
        st.pyplot(fig)

    st.subheader("Детализация")
    rows = []
    for i, seg in enumerate(segments):
        clipped = liang_barsky_clip(seg, window)
        status = "Невидим"
        vis_coords = "-"
        if clipped:
            status = "Видим"
            vis_coords = f"({clipped.p1.x:.1f}, {clipped.p1.y:.1f}) → ({clipped.p2.x:.1f}, {clipped.p2.y:.1f})"
            
        rows.append({
            "№": i + 1,
            "Исходный": f"({seg.p1.x}, {seg.p1.y}) → ({seg.p2.x}, {seg.p2.y})",
            "Статус": status,
            "Видимый сегмент": vis_coords
        })
    st.dataframe(rows, use_container_width=True)

