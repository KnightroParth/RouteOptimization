"""
Comprehensive Diagram Generator for MR Route Optimization Presentation
Generates all 16 figures from the LaTeX report matching the professional presentation theme.
Light clean canvas (#FFFFFF), dark navy text/borders (#1F2A44), elegant color hierarchy,
anti-aliased geometry, crisp vector styling, generous margins, ZERO text collisions.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle
import numpy as np
import os

OUT_DIR = r"d:\Projects\MR Route Optimization\docs\diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
C_NAVY = '#1F2A44'
C_STEEL = '#334155'
C_LIGHT_BG = '#FFFFFF'
C_BOX_BG = '#F8FAFC'
C_BOX_BORDER = '#1E3A8A'
C_ACCENT_BLUE = '#2563EB'
C_ACCENT_TEAL = '#0D9488'
C_ACCENT_RED = '#DC2626'
C_ACCENT_AMBER = '#D97706'
C_ACCENT_GREEN = '#16A34A'
C_MUTED = '#64748B'
C_LINE = '#475569'

def get_ax(w=13, h=6.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=300, facecolor=C_LIGHT_BG)
    ax.set_facecolor(C_LIGHT_BG)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax

def save(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=C_LIGHT_BG, edgecolor='none', pad_inches=0.15)
    plt.close(fig)
    print(f"Saved: {filename}")

def box(ax, x, y, w, h, title, sub=None, border=C_NAVY, fill='#F1F5F9', title_color=C_NAVY, title_size=9.5, sub_size=8, pad=0.15, lw=1.4):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=f"round,pad={pad}",
                       linewidth=lw, edgecolor=border, facecolor=fill, zorder=2)
    ax.add_patch(p)
    if sub:
        ax.text(x, y + h*0.2, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color=title_color, zorder=3)
        ax.text(x, y - h*0.22, sub, ha='center', va='center',
                fontsize=sub_size, color=C_STEEL, zorder=3, multialignment='center')
    else:
        ax.text(x, y, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color=title_color, zorder=3, multialignment='center')

def arrow(ax, x1, y1, x2, y2, color=C_LINE, lw=1.5, label=None, label_above=True, fontsize=8):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=14,
                        linewidth=lw, color=color, zorder=2)
    ax.add_patch(a)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        oy = 0.16 if label_above else -0.18
        ax.text(mx, my + oy, label, ha='center', va='center', fontsize=fontsize,
                color=C_NAVY, fontweight='bold', zorder=4,
                bbox=dict(boxstyle='square,pad=0.12', facecolor='#FFFFFF', edgecolor='none'))

def darrow(ax, points, color=C_LINE, lw=1.5):
    for i in range(len(points) - 2):
        ax.plot([points[i][0], points[i+1][0]], [points[i][1], points[i+1][1]], color=color, lw=lw, zorder=2)
    arrow(ax, points[-2][0], points[-2][1], points[-1][0], points[-1][1], color=color, lw=lw)

# ==============================================================================
# FIG 1: Problem Context
# ==============================================================================
fig, ax = get_ax(12.5, 5.0)
nodes_f1 = [
    (1.6, 3.8, 2.2, 1.2, "Multiple Doctors", "Assigned in Territory", '#1E3A8A', '#EFF6FF'),
    (4.5, 3.8, 2.2, 1.2, "Different Priorities", "Varying Commercial Value", '#B45309', '#FFFBEB'),
    (7.4, 3.8, 2.2, 1.2, "Time Windows", "Strict Clinic Availability", '#047857', '#ECFDF5'),
    (10.3, 3.8, 2.2, 1.2, "Dispersed Locations", "Geographical Distance", '#6D28D9', '#F5F3FF'),
    (6.0, 1.8, 4.2, 1.0, "Manual Planning & Ad-hoc Guesswork", "Unassisted representative routing", '#DC2626', '#FEF2F2'),
    (6.0, 0.45, 5.8, 0.7, "Outcome: Excessive Travel, Long Waiting & Missed High-Value Visits", None, '#991B1B', '#FEE2E2', '#7F1D1D')
]
for n in nodes_f1[:5]:
    box(ax, n[0], n[1], n[2], n[3], n[4], n[5], border=n[6], fill=n[7])
box(ax, nodes_f1[5][0], nodes_f1[5][1], nodes_f1[5][2], nodes_f1[5][3], nodes_f1[5][4], border=nodes_f1[5][6], fill=nodes_f1[5][7], title_color=nodes_f1[5][8], title_size=9)

arrow(ax, 2.7, 3.8, 3.4, 3.8)
arrow(ax, 5.6, 3.8, 6.3, 3.8)
arrow(ax, 8.5, 3.8, 9.2, 3.8)
darrow(ax, [(10.3, 3.2), (10.3, 2.5), (8.1, 1.8)])
darrow(ax, [(1.6, 3.2), (1.6, 2.5), (3.9, 1.8)])
darrow(ax, [(4.5, 3.2), (5.5, 2.3)])
darrow(ax, [(7.4, 3.2), (6.5, 2.3)])
arrow(ax, 6.0, 1.3, 6.0, 0.8, color=C_ACCENT_RED, lw=2.0)
save(fig, 'fig01_problem_context.png')

# ==============================================================================
# FIG 2: Research Gap & Contribution
# ==============================================================================
fig, ax = get_ax(12.8, 5.4)
f2_items = [
    (1.8, 4.0, 2.5, 1.2, "Operational &\nHistorical Data", "Doctor visits & logs", '#1E3A8A', '#EFF6FF'),
    (5.4, 4.0, 2.7, 1.2, "ML Priority Model\n(Random Forest)", "Scoring urgency & value", '#047857', '#ECFDF5'),
    (9.2, 4.0, 2.8, 1.2, "Constraints Engine\n& Travel Matrix", "Time windows & distances", '#B45309', '#FFFBEB'),
    (9.2, 1.6, 2.8, 1.2, "Route Optimizer\n(Google OR-Tools)", "VRPTW mathematical solver", '#6D28D9', '#F5F3FF'),
    (5.4, 1.6, 2.7, 1.2, "Feasible Daily Schedule", "Turn-by-turn itinerary", '#0D9488', '#F0FDFA'),
    (1.8, 1.6, 2.5, 1.2, "Role-Based Dashboards", "MR & Manager Apps", '#DC2626', '#FEF2F2')
]
for x, y, w, h, t, s, b, f in f2_items:
    box(ax, x, y, w, h, t, s, border=b, fill=f)

arrow(ax, 3.05, 4.0, 4.05, 4.0, label="Input Records")
arrow(ax, 6.75, 4.0, 7.8, 4.0, label="Priority Scores")
arrow(ax, 9.2, 3.4, 9.2, 2.2, label="Feasible Windows", label_above=False)
arrow(ax, 7.8, 1.6, 6.75, 1.6, label="Optimized Plan")
arrow(ax, 4.05, 1.6, 3.05, 1.6, label="Execution & Tracking")
save(fig, 'fig02_research_gap.png')

# ==============================================================================
# FIG 3: Project Timeline (Gantt Chart)
# ==============================================================================
fig, ax = get_ax(12.5, 5.6)
tasks = [
    ("Problem Definition & Literature Survey", 1, 3, '#1E3A8A'),
    ("Requirements Specification & Scope", 2, 4, '#0369A1'),
    ("Database Schema & Master Data Design", 3, 6, '#047857'),
    ("ML Priority Prediction Formulation", 5, 8, '#B45309'),
    ("Route Optimization (VRPTW Engine)", 7, 11, '#6D28D9'),
    ("Web Modules & Dashboard Development", 8, 13, '#0D9488'),
    ("Integration, Testing & Validation", 11, 15, '#DC2626'),
    ("Documentation & Final Defense", 13, 16, '#334155'),
]
ax.set_ylim(0, 9.5)
ax.set_xlim(0, 17.5)

for w in range(1, 17):
    ax.axvline(w, color='#E2E8F0', lw=1, zorder=1)
    ax.text(w, 8.8, f"W{w}", ha='center', va='center', fontsize=8.5, color=C_MUTED, fontweight='bold')

for idx, (name, s, e, col) in enumerate(tasks):
    y = 8.0 - idx * 0.95
    ax.text(0.2, y, name, ha='left', va='center', fontsize=9.2, color=C_NAVY, fontweight='bold')
    bar_w = e - s + 0.8
    p = FancyBboxPatch((s - 0.4, y - 0.26), bar_w, 0.52, boxstyle="round,pad=0.08",
                       linewidth=1.2, edgecolor=col, facecolor=col + '25', zorder=2)
    ax.add_patch(p)
    ax.text(s - 0.4 + bar_w/2, y, f"W{s} - W{e}", ha='center', va='center', fontsize=8, color=col, fontweight='bold', zorder=3)

save(fig, 'fig03_gantt_timeline.png')

# ==============================================================================
# FIG 4: Task Dependency Network
# ==============================================================================
fig, ax = get_ax(12.8, 5.2)
f4_nodes = [
    (1.8, 3.8, 2.4, 1.1, "Requirements & Scope", "Deliverable D1", '#1E3A8A', '#EFF6FF'),
    (5.0, 3.8, 2.5, 1.1, "Data Schema & Validation", "Deliverable D2", '#047857', '#ECFDF5'),
    (8.2, 3.8, 2.4, 1.1, "ML Priority Model", "Deliverable D3", '#B45309', '#FFFBEB'),
    (11.2, 2.6, 2.4, 1.1, "Route Optimizer\n(OR-Tools)", "Deliverable D4", '#6D28D9', '#F5F3FF'),
    (8.2, 1.4, 2.4, 1.1, "Web Dashboards\n(React Client)", "Deliverable D5", '#0D9488', '#F0FDFA'),
    (5.0, 1.4, 2.5, 1.1, "System Integration\n& Testing", "Deliverable D6", '#DC2626', '#FEF2F2'),
    (1.8, 1.4, 2.4, 1.1, "Report & Demo Defense", "Deliverable D7", '#334155', '#F1F5F9'),
]
for x, y, w, h, t, s, b, f in f4_nodes:
    box(ax, x, y, w, h, t, s, border=b, fill=f)

arrow(ax, 3.0, 3.8, 3.75, 3.8)
arrow(ax, 6.25, 3.8, 7.0, 3.8)
arrow(ax, 9.4, 3.8, 10.0, 2.8)
arrow(ax, 11.2, 2.05, 9.4, 1.4)
arrow(ax, 7.0, 1.4, 6.25, 1.4)
arrow(ax, 3.75, 1.4, 3.0, 1.4)
darrow(ax, [(5.0, 3.25), (5.0, 2.6), (7.0, 1.6)])
save(fig, 'fig04_task_network.png')

# ==============================================================================
# FIG 5: Iterative Development Model (SDLC)
# ==============================================================================
fig, ax = get_ax(12.5, 4.8)
sdlc = [
    (1.5, 3.2, 2.0, 1.1, "1. Requirements", "Scope & Constraints", '#1E3A8A', '#EFF6FF'),
    (3.9, 3.2, 2.0, 1.1, "2. System Design", "UML & Schema", '#0369A1', '#F0F9FF'),
    (6.3, 3.2, 2.0, 1.1, "3. Implementation", "ML & OR-Tools", '#047857', '#ECFDF5'),
    (8.7, 3.2, 2.0, 1.1, "4. Verification", "Integration Tests", '#B45309', '#FFFBEB'),
    (11.1, 3.2, 2.0, 1.1, "5. Review & Demo", "Panel Feedback", '#6D28D9', '#F5F3FF'),
]
for x, y, w, h, t, s, b, f in sdlc:
    box(ax, x, y, w, h, t, s, border=b, fill=f)

arrow(ax, 2.5, 3.2, 2.9, 3.2)
arrow(ax, 4.9, 3.2, 5.3, 3.2)
arrow(ax, 7.3, 3.2, 7.7, 3.2)
arrow(ax, 9.7, 3.2, 10.1, 3.2)

darrow(ax, [(11.1, 2.65), (11.1, 1.2), (1.5, 1.2), (1.5, 2.65)], color=C_ACCENT_RED, lw=1.8)
ax.text(6.3, 1.5, "Iterative Refinement Loop (Feedback & Parameter Tuning)", ha='center', va='center',
        fontsize=9, fontweight='bold', color=C_ACCENT_RED,
        bbox=dict(boxstyle='square,pad=0.2', facecolor='#FFFFFF', edgecolor='none'))
save(fig, 'fig05_sdlc_model.png')

# ==============================================================================
# FIG 6: Overall System Architecture (5 Layers)
# ==============================================================================
fig, ax = get_ax(13.0, 6.2)
layers = [
    (6.5, 5.5, 12.2, 0.9, "PRESENTATION LAYER", '#1E3A8A', '#EFF6FF'),
    (6.5, 4.2, 12.2, 0.9, "APPLICATION & API GATEWAY LAYER", '#047857', '#ECFDF5'),
    (3.5, 2.7, 5.8, 1.1, "MACHINE LEARNING LAYER", '#B45309', '#FFFBEB'),
    (9.5, 2.7, 5.8, 1.1, "OPTIMIZATION LAYER", '#6D28D9', '#F5F3FF'),
    (6.5, 0.9, 12.2, 0.9, "PERSISTENCE & DATA LAYER", '#334155', '#F1F5F9'),
]
for x, y, w, h, t, b, f in layers:
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                       linewidth=1.2, edgecolor=b, facecolor=f, zorder=1)
    ax.add_patch(p)
    ax.text(x - w/2 + 0.3, y + h/2 - 0.22, t, ha='left', va='center', fontsize=8.5,
            fontweight='bold', color=b, zorder=2)

box(ax, 3.5, 5.4, 4.0, 0.55, "MR Dashboard (React.js, Leaflet)", None, '#1E3A8A', '#FFFFFF', title_size=8.5)
box(ax, 9.5, 5.4, 4.0, 0.55, "Manager Analytics (React.js, Recharts)", None, '#1E3A8A', '#FFFFFF', title_size=8.5)

box(ax, 2.6, 4.1, 2.6, 0.55, "FastAPI REST Server", None, '#047857', '#FFFFFF', title_size=8.5)
box(ax, 6.5, 4.1, 2.8, 0.55, "JWT Auth & Role Guard", None, '#047857', '#FFFFFF', title_size=8.5)
box(ax, 10.4, 4.1, 2.8, 0.55, "Service Controllers", None, '#047857', '#FFFFFF', title_size=8.5)

box(ax, 3.5, 2.6, 4.8, 0.65, "Priority Engine (Random Forest)\nFeature Extraction & Classification", None, '#B45309', '#FFFFFF', title_size=8)
box(ax, 9.5, 2.6, 4.8, 0.65, "Route Optimizer (Google OR-Tools)\nVRPTW Solver & Travel Matrix Engine", None, '#6D28D9', '#FFFFFF', title_size=8)

box(ax, 3.5, 0.8, 4.8, 0.55, "PostgreSQL / MySQL Master Database", None, '#334155', '#FFFFFF', title_size=8.5)
box(ax, 9.5, 0.8, 4.8, 0.55, "Audit Logs, Route History & Geo-Cache", None, '#334155', '#FFFFFF', title_size=8.5)

arrow(ax, 3.5, 5.1, 3.5, 4.4)
arrow(ax, 9.5, 5.1, 9.5, 4.4)
arrow(ax, 3.5, 3.75, 3.5, 3.25)
arrow(ax, 9.5, 3.75, 9.5, 3.25)
arrow(ax, 3.5, 2.15, 3.5, 1.15)
arrow(ax, 9.5, 2.15, 9.5, 1.15)
save(fig, 'fig06_architecture.png')

# ==============================================================================
# FIG 7: End-to-End MR Data Flow
# ==============================================================================
fig, ax = get_ax(13.2, 5.2)
f7_steps = [
    (1.4, 4.0, 2.0, 1.0, "MR Login", "JWT Auth", '#1E3A8A', '#EFF6FF'),
    (3.9, 4.0, 2.1, 1.0, "Select Date &\nTerritory", "Target Filter", '#0369A1', '#F0F9FF'),
    (6.6, 4.0, 2.4, 1.0, "Fetch Doctors &\nAppointments", "Database Query", '#047857', '#ECFDF5'),
    (9.6, 4.0, 2.4, 1.0, "Feature Extraction\n& Validation", "Preprocess Data", '#B45309', '#FFFBEB'),
    (12.0, 2.6, 2.0, 1.0, "Predict Priority\n(Random Forest)", "Classify Urgency", '#6D28D9', '#F5F3FF'),
    (9.6, 1.2, 2.4, 1.0, "Compute Travel\nMatrix", "Distance / Time", '#0D9488', '#F0FDFA'),
    (6.6, 1.2, 2.4, 1.0, "OR-Tools Route\nOptimization", "VRPTW Constraints", '#DC2626', '#FEF2F2'),
    (3.9, 1.2, 2.1, 1.0, "Generate Itinerary\n& Turn-by-Turn", "Optimal Order", '#1E3A8A', '#EFF6FF'),
    (1.4, 1.2, 2.0, 1.0, "Interactive Map\nDisplay", "Leaflet Dashboard", '#047857', '#ECFDF5'),
]
for x, y, w, h, t, s, b, f in f7_steps:
    box(ax, x, y, w, h, t, s, border=b, fill=f, title_size=8.5, sub_size=7.5)

arrow(ax, 2.4, 4.0, 2.85, 4.0)
arrow(ax, 4.95, 4.0, 5.4, 4.0)
arrow(ax, 7.8, 4.0, 8.4, 4.0)
arrow(ax, 10.8, 4.0, 11.2, 3.1)
arrow(ax, 12.0, 2.1, 10.8, 1.5)
arrow(ax, 8.4, 1.2, 7.8, 1.2)
arrow(ax, 5.4, 1.2, 4.95, 1.2)
arrow(ax, 2.85, 1.2, 2.4, 1.2)
save(fig, 'fig07_data_flow.png')

# ==============================================================================
# FIG 8: Use Case UML Diagram
# ==============================================================================
fig, ax = get_ax(13.0, 6.2)
rect = FancyBboxPatch((2.6, 0.4), 7.8, 5.4, boxstyle="round,pad=0.15",
                      linewidth=1.5, edgecolor=C_NAVY, facecolor='#FAFBFD', zorder=1)
ax.add_patch(rect)
ax.text(6.5, 5.5, "SYSTEM BOUNDARY: MR VISIT PLANNING & ROUTE OPTIMIZATION",
        ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_NAVY, zorder=2)

def draw_actor(ax, x, y, label):
    ax.plot([x, x], [y - 0.2, y - 0.55], color=C_NAVY, lw=2, zorder=3)
    c = Circle((x, y), 0.18, edgecolor=C_NAVY, facecolor='#E2E8F0', lw=2, zorder=3)
    ax.add_patch(c)
    ax.plot([x - 0.3, x + 0.3], [y - 0.32, y - 0.32], color=C_NAVY, lw=2, zorder=3)
    ax.plot([x, x - 0.25], [y - 0.55, y - 0.9], color=C_NAVY, lw=2, zorder=3)
    ax.plot([x, x + 0.25], [y - 0.55, y - 0.9], color=C_NAVY, lw=2, zorder=3)
    ax.text(x, y - 1.15, label, ha='center', va='center', fontsize=9, fontweight='bold', color=C_NAVY, zorder=4)

draw_actor(ax, 1.3, 3.6, "Medical\nRepresentative\n(MR)")
draw_actor(ax, 11.7, 3.6, "Field Sales\nManager")

use_cases = [
    (4.5, 4.6, "Authenticate & Sign In", '#1E3A8A'),
    (8.5, 4.6, "Manage Doctors & Terr.", '#047857'),
    (4.5, 3.6, "View Assigned Visits", '#0369A1'),
    (8.5, 3.6, "Monitor Field Team", '#B45309'),
    (4.5, 2.6, "Request Optimized Route", '#6D28D9'),
    (8.5, 2.6, "Analyze KPI & Coverage", '#DC2626'),
    (4.5, 1.6, "Update Visit Log / Status", '#0D9488'),
    (8.5, 1.6, "Export Route Analytics", '#334155'),
]
for cx, cy, label, col in use_cases:
    ellipse = mpatches.Ellipse((cx, cy), 2.8, 0.65, edgecolor=col, facecolor='#FFFFFF', lw=1.4, zorder=2)
    ax.add_patch(ellipse)
    ax.text(cx, cy, label, ha='center', va='center', fontsize=8.2, fontweight='bold', color=col, zorder=3)

for cy in [4.6, 3.6, 2.6, 1.6]:
    ax.plot([1.6, 3.1], [3.6, cy], color=C_LINE, lw=1.2, zorder=2)
for cy in [4.6, 3.6, 2.6, 1.6]:
    ax.plot([11.4, 9.9], [3.6, cy], color=C_LINE, lw=1.2, zorder=2)

save(fig, 'fig08_use_case.png')

# ==============================================================================
# FIG 9: Activity UML Diagram
# ==============================================================================
fig, ax = get_ax(12.5, 6.2)
c_start = Circle((1.2, 5.3), 0.22, facecolor=C_NAVY, edgecolor=C_NAVY, zorder=3)
ax.add_patch(c_start)
ax.text(1.2, 5.75, "Start", ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_NAVY)

box(ax, 3.4, 5.3, 2.2, 0.8, "Sign In & Auth", "Validate Token", '#1E3A8A', '#EFF6FF', title_size=8.5)
arrow(ax, 1.45, 5.3, 2.3, 5.3)

box(ax, 6.6, 5.3, 2.4, 0.8, "Fetch Today's Visits", "Query Target Doctors", '#047857', '#ECFDF5', title_size=8.5)
arrow(ax, 4.5, 5.3, 5.4, 5.3)

box(ax, 10.0, 5.3, 2.6, 0.8, "Generate Optimized Route", "Run ML & OR-Tools", '#6D28D9', '#F5F3FF', title_size=8.5)
arrow(ax, 7.8, 5.3, 8.7, 5.3)

box(ax, 10.0, 3.6, 2.6, 0.8, "Travel to Stop Location", "Navigate Turn-by-Turn", '#0369A1', '#F0F9FF', title_size=8.5)
arrow(ax, 10.0, 4.9, 10.0, 4.0)

d = Polygon([(6.6, 3.9), (7.4, 3.6), (6.6, 3.3), (5.8, 3.6)], closed=True,
            edgecolor=C_NAVY, facecolor='#FEF3C7', lw=1.5, zorder=3)
ax.add_patch(d)
ax.text(6.6, 3.6, "Doctor\nAvailable?", ha='center', va='center', fontsize=7.5, fontweight='bold', color=C_NAVY, zorder=4)
arrow(ax, 8.7, 3.6, 7.4, 3.6)

box(ax, 6.6, 1.9, 2.4, 0.8, "Conduct Consultation", "Log Products Detailed", '#047857', '#ECFDF5', title_size=8.5)
arrow(ax, 6.6, 3.3, 6.6, 2.3, label="[Yes]")

box(ax, 3.4, 3.6, 2.2, 0.8, "Log Missed / Delay", "Record Reason", '#DC2626', '#FEF2F2', title_size=8.5)
arrow(ax, 5.8, 3.6, 4.5, 3.6, label="[No]", label_above=True)

d2 = Polygon([(3.4, 2.2), (4.1, 1.9), (3.4, 1.6), (2.7, 1.9)], closed=True,
             edgecolor=C_NAVY, facecolor='#FEF3C7', lw=1.5, zorder=3)
ax.add_patch(d2)
ax.text(3.4, 1.9, "More\nStops?", ha='center', va='center', fontsize=7.5, fontweight='bold', color=C_NAVY, zorder=4)
arrow(ax, 5.4, 1.9, 4.1, 1.9)
arrow(ax, 3.4, 3.2, 3.4, 2.2)

darrow(ax, [(3.4, 1.6), (3.4, 0.9), (10.0, 0.9), (10.0, 3.2)], color=C_ACCENT_BLUE, lw=1.5)
ax.text(6.7, 0.7, "[Yes - Next Stop]", ha='center', va='center', fontsize=8, color=C_ACCENT_BLUE, fontweight='bold')

c_end_outer = Circle((1.2, 1.9), 0.24, edgecolor=C_NAVY, facecolor='#FFFFFF', lw=2, zorder=3)
c_end_inner = Circle((1.2, 1.9), 0.14, edgecolor=C_NAVY, facecolor=C_NAVY, zorder=4)
ax.add_patch(c_end_outer)
ax.add_patch(c_end_inner)
ax.text(1.2, 2.35, "End Day", ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_NAVY)
arrow(ax, 2.7, 1.9, 1.48, 1.9, label="[No]")

save(fig, 'fig09_activity_mr.png')

# ==============================================================================
# FIG 10: Sequence UML Diagram
# ==============================================================================
fig, ax = get_ax(13.2, 6.2)
lifelines = [
    (1.2, "MR Actor"),
    (3.5, "React UI"),
    (5.9, "FastAPI API"),
    (8.3, "Database"),
    (10.7, "ML Engine"),
    (12.5, "OR-Tools")
]
for x, name in lifelines:
    box(ax, x, 5.7, 1.8, 0.6, name, None, '#1E3A8A', '#EFF6FF', title_size=8.5)
    ax.plot([x, x], [5.4, 0.4], color='#94A3B8', lw=1.2, ls='--', zorder=1)

def seq_msg(ax, x1, x2, y, label, is_ret=False):
    ls = '--' if is_ret else '-'
    col = C_ACCENT_BLUE if not is_ret else C_ACCENT_TEAL
    a = FancyArrowPatch((x1, y), (x2, y), arrowstyle='-|>', mutation_scale=12,
                        linewidth=1.4, color=col, linestyle=ls, zorder=2)
    ax.add_patch(a)
    mx = (x1 + x2) / 2
    ax.text(mx, y + 0.14, label, ha='center', va='center', fontsize=7.8,
            fontweight='bold', color=col, zorder=3,
            bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none'))

seq_msg(ax, 1.2, 3.5, 4.8, "1. Click 'Generate Route'")
seq_msg(ax, 3.5, 5.9, 4.3, "2. POST /routes/generate")
seq_msg(ax, 5.9, 8.3, 3.8, "3. Query Doctors & Appts")
seq_msg(ax, 8.3, 5.9, 3.3, "4. Doctor Records Returned", is_ret=True)
seq_msg(ax, 5.9, 10.7, 2.8, "5. predict_priority(features)")
seq_msg(ax, 10.7, 5.9, 2.3, "6. Priority Scores [H/M/L]", is_ret=True)
seq_msg(ax, 5.9, 12.5, 1.8, "7. solve_vrptw(matrix, windows)")
seq_msg(ax, 12.5, 5.9, 1.3, "8. Optimized Tour Stops", is_ret=True)
seq_msg(ax, 5.9, 8.3, 0.9, "9. Persist Route Plan")
seq_msg(ax, 5.9, 3.5, 0.6, "10. Route JSON Payload", is_ret=True)

save(fig, 'fig10_sequence_diagram.png')

# ==============================================================================
# FIG 11: Conceptual UML Class Diagram
# ==============================================================================
fig, ax = get_ax(13.2, 6.2)

def uml_class(ax, x, y, w, h, name, attrs, methods, col='#1E3A8A'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                       linewidth=1.4, edgecolor=col, facecolor='#FFFFFF', zorder=2)
    ax.add_patch(p)
    header_h = 0.55
    hp = Rectangle((x - w/2, y + h/2 - header_h), w, header_h,
                   facecolor=col + '18', edgecolor='none', zorder=2)
    ax.add_patch(hp)
    ax.text(x, y + h/2 - 0.28, name, ha='center', va='center', fontsize=9, fontweight='bold', color=col, zorder=3)
    ax.plot([x - w/2, x + w/2], [y + h/2 - header_h, y + h/2 - header_h], color=col, lw=1.2, zorder=3)
    
    attr_y = y + h/2 - header_h - 0.2
    for a in attrs:
        ax.text(x - w/2 + 0.15, attr_y, f"+ {a}", ha='left', va='center', fontsize=7.2, color=C_STEEL, zorder=3)
        attr_y -= 0.22
    
    div_y = y - h/2 + len(methods)*0.22 + 0.15
    ax.plot([x - w/2, x + w/2], [div_y, div_y], color=col, lw=0.8, ls='--', zorder=3)
    
    meth_y = div_y - 0.2
    for m in methods:
        ax.text(x - w/2 + 0.15, meth_y, f"+ {m}()", ha='left', va='center', fontsize=7.2, color=col, fontweight='semibold', zorder=3)
        meth_y -= 0.22

uml_class(ax, 1.8, 4.6, 2.8, 1.8, "User", ["user_id: int", "email: string", "role: string"], ["login()", "validate_token()"], '#1E3A8A')
uml_class(ax, 5.2, 4.6, 3.0, 1.8, "MedicalRep", ["mr_id: int", "territory: string", "max_hours: float"], ["request_route()", "get_status()"], '#047857')
uml_class(ax, 8.8, 4.6, 3.2, 1.8, "Doctor", ["doctor_id: int", "specialty: string", "lat, lon: float", "window_start, end: time"], ["get_schedule()"], '#B45309')
uml_class(ax, 12.0, 4.6, 2.6, 1.8, "PriorityPrediction", ["pred_id: int", "score: float", "class: string"], ["predict()", "explain()"], '#6D28D9')

uml_class(ax, 3.5, 1.7, 3.2, 1.9, "Route", ["route_id: int", "mr_id: int", "date: date", "total_dist, time: float"], ["optimize()", "export()"], '#0D9488')
uml_class(ax, 7.4, 1.7, 3.2, 1.9, "RouteStop", ["stop_id: int", "route_id: int", "doctor_id: int", "seq: int", "eta, etd: time"], ["mark_visited()"], '#DC2626')
uml_class(ax, 11.2, 1.7, 2.8, 1.9, "VisitRecord", ["visit_id: int", "status: string", "notes: text"], ["complete()", "reschedule()"], '#334155')

ax.plot([3.2, 3.7], [4.6, 4.6], color=C_LINE, lw=1.2)
ax.plot([6.7, 7.2], [4.6, 4.6], color=C_LINE, lw=1.2)
ax.plot([10.4, 10.7], [4.6, 4.6], color=C_LINE, lw=1.2)
ax.plot([5.1, 7.4], [1.7, 1.7], color=C_LINE, lw=1.2)
ax.plot([9.0, 9.8], [1.7, 1.7], color=C_LINE, lw=1.2)
ax.plot([5.2, 3.5], [3.7, 2.65], color=C_LINE, lw=1.2)
ax.plot([8.8, 7.4], [3.7, 2.65], color=C_LINE, lw=1.2)

save(fig, 'fig11_class_diagram.png')

# ==============================================================================
# FIG 12: Entity-Relationship (ER) Diagram
# ==============================================================================
fig, ax = get_ax(13.2, 6.0)

def er_table(ax, x, y, w, h, name, fields, col='#1E3A8A'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                       linewidth=1.4, edgecolor=col, facecolor='#FFFFFF', zorder=2)
    ax.add_patch(p)
    header_h = 0.5
    hp = Rectangle((x - w/2, y + h/2 - header_h), w, header_h,
                   facecolor=col + '20', edgecolor='none', zorder=2)
    ax.add_patch(hp)
    ax.text(x, y + h/2 - 0.25, name, ha='center', va='center', fontsize=8.8, fontweight='bold', color=col, zorder=3)
    ax.plot([x - w/2, x + w/2], [y + h/2 - header_h, y + h/2 - header_h], color=col, lw=1.2, zorder=3)
    
    fy = y + h/2 - header_h - 0.22
    for f in fields:
        is_key = f.startswith('PK') or f.startswith('FK')
        clr = col if is_key else C_STEEL
        weight = 'bold' if is_key else 'normal'
        ax.text(x - w/2 + 0.15, fy, f, ha='left', va='center', fontsize=7.2, color=clr, fontweight=weight, zorder=3)
        fy -= 0.23

er_table(ax, 1.8, 4.5, 2.6, 2.0, "USERS", ["PK user_id", "email VARCHAR", "password_hash", "role ENUM", "created_at"], '#1E3A8A')
er_table(ax, 5.4, 4.5, 2.8, 2.0, "MEDICAL_REPS", ["PK mr_id", "FK user_id", "territory VARCHAR", "start_lat, lon", "work_hours_limit"], '#047857')
er_table(ax, 9.2, 4.5, 2.8, 2.2, "DOCTORS", ["PK doctor_id", "name VARCHAR", "specialization", "lat, lon DECIMAL", "avail_start, end", "avg_duration_min"], '#B45309')
er_table(ax, 12.3, 4.5, 2.4, 1.8, "PREDICTIONS", ["PK pred_id", "FK doctor_id", "priority_score", "priority_level", "model_version"], '#6D28D9')

er_table(ax, 3.6, 1.5, 2.8, 2.0, "ROUTES", ["PK route_id", "FK mr_id", "plan_date DATE", "total_distance_km", "total_duration_min", "status VARCHAR"], '#0D9488')
er_table(ax, 7.6, 1.5, 3.0, 2.2, "ROUTE_STOPS", ["PK stop_id", "FK route_id", "FK doctor_id", "sequence_order INT", "est_arrival TIME", "est_departure TIME", "status ENUM"], '#DC2626')
er_table(ax, 11.4, 1.5, 2.6, 1.8, "VISIT_LOGS", ["PK visit_id", "FK doctor_id", "FK mr_id", "visit_date DATE", "outcome VARCHAR"], '#334155')

def er_rel(ax, x1, y1, x2, y2, label):
    ax.plot([x1, x2], [y1, y2], color=C_LINE, lw=1.2, zorder=2)
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    ax.text(mx, my, label, ha='center', va='center', fontsize=7.2, color='#1E293B',
            fontweight='bold', bbox=dict(boxstyle='square,pad=0.1', facecolor='#F1F5F9', edgecolor='none'), zorder=3)

er_rel(ax, 3.1, 4.5, 4.0, 4.5, "1 : 1")
er_rel(ax, 6.8, 4.5, 7.8, 4.5, "1 : N")
er_rel(ax, 10.6, 4.5, 11.1, 4.5, "1 : N")
er_rel(ax, 5.0, 1.5, 6.1, 1.5, "1 : N")
er_rel(ax, 9.1, 1.5, 10.1, 1.5, "1 : N")
er_rel(ax, 5.4, 3.5, 3.6, 2.5, "1 : N")
er_rel(ax, 9.2, 3.4, 7.6, 2.6, "1 : N")

save(fig, 'fig12_er_diagram.png')

# ==============================================================================
# FIG 13: State Machine Diagram (Route Lifecycle)
# ==============================================================================
fig, ax = get_ax(12.8, 4.8)
c13_start = Circle((1.0, 3.2), 0.2, facecolor=C_NAVY, edgecolor=C_NAVY, zorder=3)
ax.add_patch(c13_start)

box(ax, 2.8, 3.2, 2.2, 0.9, "Draft Request", "Input Selection", '#1E3A8A', '#EFF6FF', title_size=8.5)
arrow(ax, 1.2, 3.2, 1.7, 3.2)

box(ax, 5.8, 3.2, 2.2, 0.9, "Validated", "Constraints Met", '#047857', '#ECFDF5', title_size=8.5)
arrow(ax, 3.9, 3.2, 4.7, 3.2, label="Valid Input")

box(ax, 8.8, 3.2, 2.4, 0.9, "Optimized / Scheduled", "VRPTW Solved", '#6D28D9', '#F5F3FF', title_size=8.5)
arrow(ax, 6.9, 3.2, 7.6, 3.2, label="Solve Route")

box(ax, 11.5, 3.2, 2.0, 0.9, "In Progress", "MR En Route", '#0D9488', '#F0FDFA', title_size=8.5)
arrow(ax, 10.0, 3.2, 10.5, 3.2, label="Start Day")

box(ax, 5.8, 1.2, 2.2, 0.8, "Validation Failed", "Conflict Found", '#DC2626', '#FEF2F2', title_size=8)
arrow(ax, 2.8, 2.75, 5.0, 1.4, label="[Invalid]", color=C_ACCENT_RED)
arrow(ax, 5.8, 1.6, 3.5, 2.8, label="[Fix Params]", color=C_ACCENT_BLUE)

box(ax, 11.5, 1.2, 2.0, 0.8, "Completed", "All Stops Done", '#047857', '#ECFDF5', title_size=8.5)
arrow(ax, 11.5, 2.75, 11.5, 1.6, label="Finish")

c13_end_outer = Circle((9.5, 1.2), 0.22, edgecolor=C_NAVY, facecolor='#FFFFFF', lw=2, zorder=3)
c13_end_inner = Circle((9.5, 1.2), 0.13, edgecolor=C_NAVY, facecolor=C_NAVY, zorder=4)
ax.add_patch(c13_end_outer)
ax.add_patch(c13_end_inner)
arrow(ax, 10.5, 1.2, 9.75, 1.2)

save(fig, 'fig13_state_diagram.png')

# ==============================================================================
# FIG 14: Component Diagram
# ==============================================================================
fig, ax = get_ax(13.2, 5.8)

def comp_box(ax, x, y, w, h, name, sub, col='#1E3A8A', fill='#EFF6FF'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                       linewidth=1.4, edgecolor=col, facecolor=fill, zorder=2)
    ax.add_patch(p)
    tab1 = Rectangle((x - w/2 - 0.15, y + h*0.12), 0.3, 0.18, facecolor=fill, edgecolor=col, lw=1.2, zorder=3)
    tab2 = Rectangle((x - w/2 - 0.15, y - h*0.28), 0.3, 0.18, facecolor=fill, edgecolor=col, lw=1.2, zorder=3)
    ax.add_patch(tab1)
    ax.add_patch(tab2)
    ax.text(x, y + 0.15, name, ha='center', va='center', fontsize=8.8, fontweight='bold', color=col, zorder=4)
    ax.text(x, y - 0.2, sub, ha='center', va='center', fontsize=7.5, color=C_STEEL, zorder=4)

comp_box(ax, 2.0, 3.2, 3.2, 1.4, "React Web Application", "UI / GIS Visualization", '#1E3A8A', '#EFF6FF')
comp_box(ax, 6.2, 3.2, 3.2, 1.4, "FastAPI REST API", "Gateway & Controllers", '#047857', '#ECFDF5')
comp_box(ax, 10.8, 4.6, 3.2, 1.3, "ML Priority Engine", "Random Forest Service", '#B45309', '#FFFBEB')
comp_box(ax, 10.8, 3.0, 3.2, 1.3, "Route Optimizer", "Google OR-Tools VRPTW", '#6D28D9', '#F5F3FF')
comp_box(ax, 10.8, 1.4, 3.2, 1.3, "Persistence Layer", "PostgreSQL / MySQL DB", '#334155', '#F1F5F9')

arrow(ax, 3.6, 3.2, 4.6, 3.2, label="REST / JSON")
arrow(ax, 7.8, 3.5, 9.2, 4.5, label="predict()")
arrow(ax, 7.8, 3.2, 9.2, 3.1, label="solve_vrptw()")
arrow(ax, 7.8, 2.9, 9.2, 1.7, label="ORM Queries")

save(fig, 'fig14_component_diagram.png')

# ==============================================================================
# FIG 15: Deployment Diagram
# ==============================================================================
fig, ax = get_ax(13.0, 5.2)

def deploy_node(ax, x, y, w, h, name, sub, col='#1E3A8A', fill='#F8FAFC'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.12",
                       linewidth=1.4, edgecolor=col, facecolor=fill, zorder=2)
    ax.add_patch(p)
    ax.text(x, y + h*0.25, f"<<device / node>>", ha='center', va='center', fontsize=7.5, color=C_MUTED, zorder=3)
    ax.text(x, y + 0.05, name, ha='center', va='center', fontsize=9.2, fontweight='bold', color=col, zorder=3)
    ax.text(x, y - h*0.25, sub, ha='center', va='center', fontsize=7.8, color=C_STEEL, zorder=3)

deploy_node(ax, 2.0, 2.6, 3.2, 2.0, "Client Workstation\n/ Smartphone", "Modern Web Browser\n(Chromium / Safari)", '#1E3A8A', '#EFF6FF')
deploy_node(ax, 6.5, 2.6, 3.4, 2.0, "Application Server\n(Docker / Cloud VM)", "FastAPI + Uvicorn ASGI\nPython 3.12 Runtime", '#047857', '#ECFDF5')
deploy_node(ax, 11.0, 4.0, 3.0, 1.6, "Database Server", "PostgreSQL / MySQL\nManaged DB Host", '#334155', '#F1F5F9')
deploy_node(ax, 11.0, 1.4, 3.0, 1.6, "GIS / Map Provider", "OSRM / Mapbox / OSM\nTravel Matrix API", '#6D28D9', '#F5F3FF')

arrow(ax, 3.6, 2.6, 4.8, 2.6, label="HTTPS / TLS 1.3")
arrow(ax, 8.2, 3.1, 9.5, 3.8, label="TCP / SSL (5432)")
arrow(ax, 8.2, 2.1, 9.5, 1.6, label="HTTPS REST")

save(fig, 'fig15_deployment_diagram.png')

# ==============================================================================
# FIG 16: Priority Prediction ML Pipeline
# ==============================================================================
fig, ax = get_ax(13.2, 5.0)
f16_nodes = [
    (1.4, 2.8, 2.2, 1.3, "1. Raw Records", "Historical Visits &\nAppointments", '#1E3A8A', '#EFF6FF'),
    (3.8, 2.8, 2.2, 1.3, "2. Cleaning & Prep", "Impute Missing &\nScale Numerical", '#0369A1', '#F0F9FF'),
    (6.2, 2.8, 2.2, 1.3, "3. Feature Eng.", "Days Elapsed, Freq,\nDoctor Tier Index", '#047857', '#ECFDF5'),
    (8.6, 2.8, 2.2, 1.3, "4. Train / Eval", "Stratified Split &\nRandom Forest", '#B45309', '#FFFBEB'),
    (11.4, 2.8, 2.6, 1.3, "5. Inference Output", "Class: High/Med/Low\nConfidence Score", '#6D28D9', '#F5F3FF'),
]
for x, y, w, h, t, s, b, f in f16_nodes:
    box(ax, x, y, w, h, t, s, border=b, fill=f, title_size=8.5, sub_size=7.5)

arrow(ax, 2.5, 2.8, 2.7, 2.8)
arrow(ax, 4.9, 2.8, 5.1, 2.8)
arrow(ax, 7.3, 2.8, 7.5, 2.8)
arrow(ax, 9.7, 2.8, 10.1, 2.8)

save(fig, 'fig16_ml_pipeline.png')

print("All 16 diagrams generated successfully in docs/diagrams/!")
