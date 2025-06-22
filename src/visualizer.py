# src/visualizer.py

import plotly.graph_objects as go
import plotly.express as px
import os
import uuid

CHART_DIR = "static"

def _save_plotly_chart(fig, title: str):
    filename = f"{title.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.html"
    filepath = os.path.join(CHART_DIR, filename)
    fig.write_html(filepath, include_plotlyjs='cdn', full_html=False)
    return filename

def plot_line_graph(data: dict, title: str, x_label: str, y_label: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(data.keys()), 
        y=list(data.values()), 
        mode='lines+markers', 
        name=title
    ))
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    return _save_plotly_chart(fig, title)

def plot_bar_chart(data: dict, title: str, x_label: str, y_label: str):
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        labels={'x': x_label, 'y': y_label},
        title=title
    )
    return _save_plotly_chart(fig, title)

def plot_pie_chart(data: dict, title: str):
    fig = px.pie(
        names=list(data.keys()), 
        values=list(data.values()), 
        title=title
    )
    return _save_plotly_chart(fig, title)
