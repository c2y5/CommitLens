# src/visualiser.py

import plotly.graph_objects as go
import plotly.express as px
import os
import uuid
import threading

CHART_DIR = "static"

def _save_plotly_chart(fig, title: str):
    filename = f"{title.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.html"
    filepath = os.path.join(CHART_DIR, filename)
    fig.write_html(filepath, include_plotlyjs='cdn', full_html=False)

    _delete_file_after_delay(filepath, delay=60)
    return filename

def plot_line_graph(data: dict, title: str, xlabel: str, ylabel: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(data.keys()), y=list(data.values()), mode='lines+markers', name=title))
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    return _save_plotly_chart(fig, title)

def plot_bar_chart(data: dict, title: str, xlabel: str, ylabel: str):
    fig = px.bar(x=list(data.keys()), y=list(data.values()), labels={'x': xlabel, 'y': ylabel}, title=title)
    return _save_plotly_chart(fig, title)

def plot_pie_chart(data: dict, title: str):
    fig = px.pie(names=list(data.keys()), values=list(data.values()), title=title)
    return _save_plotly_chart(fig, title)

def _delete_file_after_delay(path, delay=60):
    def delete():
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"❌ Error deleting {path}: {e}")
    threading.Timer(delay, delete).start()
