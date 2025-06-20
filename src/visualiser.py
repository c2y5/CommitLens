# src/visualiser.py

import matplotlib.pyplot as plt

def plot_line_graph(data: dict, title: str, xlabel: str, ylabel: str):
    x = list(data.keys())
    y = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='o', color='tab:blue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    return fig


def plot_bar_chart(data: dict, title: str, xlabel: str, ylabel: str):
    x = list(data.keys())
    y = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x, y, color='tab:green')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    return fig


def plot_pie_chart(data: dict, title: str):
    labels = list(data.keys())
    sizes = list(data.values())

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(title)
    plt.tight_layout()
    return fig
