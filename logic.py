from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass(slots=True)
class Point:
    x: float
    y: float


@dataclass(slots=True)
class Segment:
    p1: Point
    p2: Point


@dataclass(slots=True)
class ClipWindow:
    x_min: float
    y_min: float
    x_max: float
    y_max: float


def liang_barsky_clip(segment: Segment, window: ClipWindow) -> Optional[Segment]:
    """
    Алгоритм Лианга-Барски для отсечения отрезка прямоугольным окном.
    Возвращает новый Segment (видимую часть) или None, если отрезок полностью невидим.
    """
    x1, y1 = segment.p1.x, segment.p1.y
    x2, y2 = segment.p2.x, segment.p2.y
    
    dx = x2 - x1
    dy = y2 - y1
    
    p = [-dx, dx, -dy, dy]
    q = [
        x1 - window.x_min,
        window.x_max - x1,
        y1 - window.y_min,
        window.y_max - y1
    ]
    
    t0 = 0.0
    t1 = 1.0
    
    for i in range(4):
        if p[i] == 0:
            # Отрезок параллелен границе
            if q[i] < 0:
                # Отрезок полностью за пределами границы
                return None
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                # Внешняя -> внутренняя
                if t > t1:
                    return None
                if t > t0:
                    t0 = t
            else:
                # Внутренняя -> внешняя
                if t < t0:
                    return None
                if t < t1:
                    t1 = t
                    
    if t0 > t1:
        return None
        
    new_x1 = x1 + t0 * dx
    new_y1 = y1 + t0 * dy
    new_x2 = x1 + t1 * dx
    new_y2 = y1 + t1 * dy
    
    return Segment(Point(new_x1, new_y1), Point(new_x2, new_y2))


def parse_input_data(text: str) -> Tuple[List[Segment], Optional[ClipWindow]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return [], None
        
    try:
        # Первая строка мб n, но формат может варьироваться.
        # Ищем n
        try:
            n_segments = int(lines[0])
            start_idx = 1
        except ValueError:
             # Возможно первая строка сразу координаты
             n_segments = -1
             start_idx = 0
             
        segments = []
        window = None
        
        # Читаем все строки как координаты, пока не дойдем до последней (окно)
        # Если n задано явно, читаем n строк
        
        data_lines = lines[start_idx:]
        
        if n_segments > 0:
             segment_lines = data_lines[:n_segments]
             window_line = data_lines[n_segments] if len(data_lines) > n_segments else None
        else:
            # Эвристика: последняя строка - окно, остальные - отрезки
            if len(data_lines) < 2:
                return [], None
            segment_lines = data_lines[:-1]
            window_line = data_lines[-1]
            
        for line in segment_lines:
            parts = list(map(float, line.split()))
            if len(parts) >= 4:
                segments.append(Segment(Point(parts[0], parts[1]), Point(parts[2], parts[3])))
                
        if window_line:
            w_parts = list(map(float, window_line.split()))
            if len(w_parts) >= 4:
                window = ClipWindow(
                    min(w_parts[0], w_parts[2]),
                    min(w_parts[1], w_parts[3]),
                    max(w_parts[0], w_parts[2]),
                    max(w_parts[1], w_parts[3])
                )
                
        return segments, window
        
    except (ValueError, IndexError):
        return [], None

