"""
Generate all 16 professional engineering diagrams from the LaTeX report for PPT.
Clean light theme matching the PowerPoint template:
- Canvas: White (#FFFFFF)
- Text: Dark Charcoal (#1A202C) / Dark Navy (#1F2A44)
- Node borders: Navy (#1F2A44) / Steel (#4A5568) / Blue (#2B6CB0)
- Accents: Terracotta (#C8553D), Emerald (#2F855A), Slate (#718096)
- Font: Arial / Segoe UI / sans-serif with bold headers and legible labels
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon
import numpy as np
import os

OUT_DIR = r"d:\Projects\MR Route Optimization\docs\diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_FAMILY = 'DejaVu Sans'

def setup_canvas(width=12, height=6.5):
    fig, ax = plt.subplots(figsize=(width, height), dpi=300, facecolor='#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')
    return fig, ax

def draw_card(ax, x, y, w, h, title, subtitle=None, border_color='#1F2A44', fill_color='#F7FAFC', text_color='#1A202C', lw=1.5, radius=0.15, fontsize=9.5, sub_fontsize=8):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle=f"round,pad={radius}",
                          linewidth=lw, edgecolor=border_color,
                          facecolor=fill_color, zorder=2)
    ax.add_patch(box)
    if subtitle:
        ax.text(x, y + h*0.18, title, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color,
                fontfamily=FONT_FAMILY, zorder=3)
        ax.text(x, y - h*0.20, subtitle, ha='center', va='center',
                fontsize=sub_fontsize, color='#4A5568',
                fontfamily=FONT_FAMILY, zorder=3, multialignment='center')
    else:
        ax.text(x, y, title, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color,
                fontfamily=FONT_FAMILY, zorder=3, multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, color='#1F2A44', lw=1.5, label=None, label_pos='above', fontsize=8):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='-|>',
                            mutation_scale=14,
                            linewidth=lw,
                            color=color,
                            zorder=2)
    ax.add_patch(arrow)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        offset_y = 0.15 if label_pos == 'above' else -0.18
        ax.text(mx, my + offset_y, label, ha='center', va='center',
                fontsize=fontsize, color='#2D3748', fontweight='semibold',
                fontfamily=FONT_FAMILY, zorder=4,
                bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none'))

print("Diagram generator framework ready.")
