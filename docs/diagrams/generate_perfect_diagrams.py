"""
Master Professional Diagram Generator for Review III Presentation
Generates all 16 diagrams matching the LaTeX report and PPT theme.
- Pure white background (#FFFFFF)
- Professional engineering colors (Navy #1E3A8A, Slate #334155, Crimson #991B1B, Forest Green #065F46, Amber #92400E, Indigo #4338CA)
- Zero text clipping, zero border collisions
- Clean orthogonal routing, consistent fonts, perfectly centered text
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
FONT = 'DejaVu Sans'

def new_canvas(w=14.0, h=7.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=300, facecolor='#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax

def save(fig, filename):
    p = os.path.join(OUT_DIR, filename)
    fig.savefig(p, dpi=300, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none', pad_inches=0.2)
    plt.close(fig)
    print(f"Generated: {filename}")

def card(ax, x, y, w, h, title, sub=None, border='#1E3A8A', fill='#F8FAFC', t_col='#0F172A', t_size=9.5, s_size=8.0, lw=1.4, rad=0.12):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=f"round,pad={rad}",
                       linewidth=lw, edgecolor=border, facecolor=fill, zorder=3)
    ax.add_patch(p)
    if sub:
        ax.text(x, y + h*0.22, title, ha='center', va='center',
                fontsize=t_size, fontweight='bold', color=t_col, fontfamily=FONT, zorder=4)
        ax.text(x, y - h*0.20, sub, ha='center', va='center',
                fontsize=s_size, color='#475569', fontfamily=FONT, zorder=4, multialignment='center')
    else:
        ax.text(x, y, title, ha='center', va='center',
                fontsize=t_size, fontweight='bold', color=t_col, fontfamily=FONT, zorder=4, multialignment='center')

def arrow(ax, x1, y1, x2, y2, color='#334155', lw=1.5, label=None, label_above=True, l_size=7.8):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=14,
                        linewidth=lw, color=color, zorder=5)
    ax.add_patch(a)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        oy = 0.20 if label_above else -0.22
        ax.text(mx, my + oy, label, ha='center', va='center', fontsize=l_size,
                color='#0F172A', fontweight='bold', fontfamily=FONT, zorder=6,
                bbox=dict(boxstyle='square,pad=0.12', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.7))

def ortho_arrow(ax, pts, color='#334155', lw=1.5, label=None, l_pos=None):
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]], color=color, lw=lw, zorder=4)
    arrow(ax, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], color=color, lw=lw)
    if label and l_pos:
        ax.text(l_pos[0], l_pos[1], label, ha='center', va='center', fontsize=7.8,
                color='#0F172A', fontweight='bold', fontfamily=FONT, zorder=6,
                bbox=dict(boxstyle='square,pad=0.12', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.7))

# ==============================================================================
# FIG 1: Problem Context
# ==============================================================================
fig, ax = new_canvas(14.0, 7.2)
f1_cards = [
    (1.8, 5.5, 2.4, 1.4, "Multiple Doctors", "Assigned in Territory\nDiverse Specialty Mix", '#1E3A8A', '#EFF6FF'),
    (5.3, 5.5, 2.4, 1.4, "Varying Priorities", "Strategic / Revenue Impact\nHigh vs Low Urgency", '#92400E', '#FEF3C7'),
    (8.8, 5.5, 2.4, 1.4, "Time Windows", "Strict Consultation Hours\nNarrow Visiting Slots", '#065F46', '#D1FAE5'),
    (12.2, 5.5, 2.4, 1.4, "Dispersed Locations", "Geographical Spread\nUrban Traffic Congestion", '#4338CA', '#EDE9FE'),
]
for x, y, w, h, t, s, b, f in f1_cards:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=9.5, s_size=8.0)

arrow(ax, 3.1, 5.5, 4.0, 5.5, color='#64748B')
arrow(ax, 6.6, 5.5, 7.5, 5.5, color='#64748B')
arrow(ax, 10.1, 5.5, 10.9, 5.5, color='#64748B')

card(ax, 7.0, 3.2, 6.2, 1.4, "Manual Planning & Ad-hoc Sequencing",
     "Representative relies on intuition, memory, or static spreadsheets\nInability to co-optimize visit value against travel distance & clinic availability",
     border='#B91C1C', fill='#FEF2F2', t_col='#991B1B', t_size=10.5, s_size=8.2, rad=0.15)

ortho_arrow(ax, [(1.8, 4.7), (1.8, 3.5), (3.8, 3.5)], color='#94A3B8')
ortho_arrow(ax, [(5.3, 4.7), (5.3, 3.9)], color='#94A3B8')
ortho_arrow(ax, [(8.8, 4.7), (8.8, 3.9)], color='#94A3B8')
ortho_arrow(ax, [(12.2, 4.7), (12.2, 3.5), (10.2, 3.5)], color='#94A3B8')

arrow(ax, 7.0, 2.4, 7.0, 1.6, color='#B91C1C', lw=2.0)
card(ax, 7.0, 1.0, 10.2, 1.1, "Sub-optimal Field Execution Outcomes",
     "Excessive Travel Times  ·  Prolonged Waiting at Clinics  ·  Missed High-Priority Doctor Visits  ·  MR Burnout",
     border='#991B1B', fill='#FEE2E2', t_col='#7F1D1D', t_size=10.0, s_size=8.5, lw=1.8)
save(fig, 'fig01_problem_context.png')

# ==============================================================================
# FIG 2: Research Gap & Contribution
# ==============================================================================
fig, ax = new_canvas(14.0, 6.2)
f2_boxes = [
    (1.8, 4.6, 2.4, 1.3, "Historical & Visit Data", "Doctor logs & interaction trends", '#1E3A8A', '#EFF6FF'),
    (5.4, 4.6, 2.6, 1.3, "ML Priority Model", "Random Forest scoring urgency", '#065F46', '#ECFDF5'),
    (9.2, 4.6, 2.8, 1.3, "Operational Constraints", "Time windows & travel matrix", '#92400E', '#FEF3C7'),
    (12.3, 3.0, 2.2, 1.4, "OR-Tools Solver", "VRPTW mathematical\noptimization engine", '#4338CA', '#EDE9FE'),
    (8.2, 1.4, 3.2, 1.3, "Feasible Daily Schedule", "Time-stamped sequenced itinerary", '#0D9488', '#F0FDFA'),
    (2.8, 1.4, 3.6, 1.3, "Role-Based Dashboards", "MR navigation & Manager analytics", '#1E3A8A', '#EFF6FF'),
]
for x, y, w, h, t, s, b, f in f2_boxes:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=9, s_size=7.8)

arrow(ax, 3.1, 4.6, 4.0, 4.6, label="Training Data")
arrow(ax, 6.8, 4.6, 7.7, 4.6, label="Priority Scores")
ortho_arrow(ax, [(10.7, 4.6), (12.3, 4.6), (12.3, 3.8)], label="Constraints")
ortho_arrow(ax, [(12.3, 2.2), (12.3, 1.4), (9.9, 1.4)], label="Optimized Plan", l_pos=(11.3, 1.4))
arrow(ax, 6.5, 1.4, 4.7, 1.4, label="Daily Execution")
save(fig, 'fig02_research_gap.png')

# ==============================================================================
# FIG 3: Project Timeline (Gantt Chart)
# ==============================================================================
fig, ax = new_canvas(14.0, 7.0)
tasks = [
    ("Problem Definition & Literature Survey", 1, 3, '#1E3A8A'),
    ("Requirements Specification & Scope", 2, 4, '#0369A1'),
    ("Database Schema & Master Data Design", 3, 6, '#065F46'),
    ("ML Priority Prediction Formulation", 5, 8, '#92400E'),
    ("Route Optimization (VRPTW Engine)", 7, 11, '#4338CA'),
    ("Web Modules & Dashboard Development", 8, 13, '#0D9488'),
    ("Integration, Testing & Validation", 11, 15, '#B91C1C'),
    ("Documentation & Review III Defense", 13, 16, '#334155'),
]
ax.set_ylim(0, 9.8)
ax.set_xlim(0, 17.5)

for w in range(1, 17):
    ax.axvline(w, color='#F1F5F9', lw=1.5, zorder=1)
    ax.text(w, 9.1, f"W{w}", ha='center', va='center', fontsize=9.0, color='#64748B', fontweight='bold')

for idx, (name, s, e, col) in enumerate(tasks):
    y = 8.1 - idx * 0.95
    # Row zebra background
    bg_band = Rectangle((0.2, y - 0.38), 17.0, 0.76, facecolor='#F8FAFC' if idx%2==0 else '#FFFFFF', edgecolor='none', zorder=1)
    ax.add_patch(bg_band)
    ax.text(0.4, y, name, ha='left', va='center', fontsize=9.2, color='#0F172A', fontweight='bold', zorder=2)
    bar_w = e - s + 0.8
    p = FancyBboxPatch((s - 0.4, y - 0.22), bar_w, 0.44, boxstyle="round,pad=0.06",
                       linewidth=1.2, edgecolor=col, facecolor=col + '28', zorder=3)
    ax.add_patch(p)
    ax.text(s - 0.4 + bar_w/2, y, f"W{s} - W{e}", ha='center', va='center', fontsize=8.0, color=col, fontweight='bold', zorder=4)

save(fig, 'fig03_gantt_timeline.png')

# ==============================================================================
# FIG 4: Task Dependency Network
# ==============================================================================
fig, ax = new_canvas(14.0, 6.2)
f4_nodes = [
    (1.8, 4.5, 2.4, 1.2, "Requirements & Scope", "Task T1: Scope freeze", '#1E3A8A', '#EFF6FF'),
    (5.2, 4.5, 2.5, 1.2, "Data Schema & Validation", "Task T2: PostgreSQL/Supabase", '#065F46', '#ECFDF5'),
    (8.6, 4.5, 2.5, 1.2, "ML Priority Model", "Task T3: Baseline classifier", '#92400E', '#FEF3C7'),
    (12.0, 3.0, 2.4, 1.2, "Route Optimizer", "Task T4: OR-Tools solver", '#4338CA', '#EDE9FE'),
    (8.6, 1.5, 2.5, 1.2, "Web Dashboards", "Task T5: React / Leaflet", '#0D9488', '#F0FDFA'),
    (5.2, 1.5, 2.5, 1.2, "System Integration", "Task T6: E2E pipeline & tests", '#B91C1C', '#FEF2F2'),
    (1.8, 1.5, 2.4, 1.2, "Evaluation & Defense", "Task T7: Review III deliverables", '#334155', '#F1F5F9'),
]
for x, y, w, h, t, s, b, f in f4_nodes:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=8.8, s_size=7.6)

arrow(ax, 3.1, 4.5, 3.85, 4.5)
arrow(ax, 6.55, 4.5, 7.25, 4.5)
ortho_arrow(ax, [(9.95, 4.5), (10.7, 4.5), (10.7, 3.0)])
ortho_arrow(ax, [(12.0, 2.3), (12.0, 1.5), (10.0, 1.5)])
arrow(ax, 7.25, 1.5, 6.55, 1.5)
arrow(ax, 3.85, 1.5, 3.1, 1.5)
ortho_arrow(ax, [(5.2, 3.8), (5.2, 2.8), (7.25, 1.8)], label="API feeds")
save(fig, 'fig04_task_network.png')

# ==============================================================================
# FIG 5: Iterative Development Model (SDLC)
# ==============================================================================
fig, ax = new_canvas(14.0, 5.5)
sdlc = [
    (1.5, 3.6, 2.0, 1.2, "1. Requirements", "Scope, metrics, constraints", '#1E3A8A', '#EFF6FF'),
    (4.0, 3.6, 2.0, 1.2, "2. System Design", "UML, schema, architecture", '#0369A1', '#F0F9FF'),
    (6.5, 3.6, 2.0, 1.2, "3. Implementation", "ML model, OR-Tools, UI", '#065F46', '#ECFDF5'),
    (9.0, 3.6, 2.0, 1.2, "4. Verification", "Integration & test suite", '#92400E', '#FEF3C7'),
    (11.5, 3.6, 2.0, 1.2, "5. Review & Demo", "Evaluation & feedback", '#4338CA', '#EDE9FE'),
]
for x, y, w, h, t, s, b, f in sdlc:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=8.8, s_size=7.5)

arrow(ax, 2.6, 3.6, 2.9, 3.6)
arrow(ax, 5.1, 3.6, 5.4, 3.6)
arrow(ax, 7.6, 3.6, 7.9, 3.6)
arrow(ax, 10.1, 3.6, 10.4, 3.6)

ortho_arrow(ax, [(11.5, 2.9), (11.5, 1.3), (1.5, 1.3), (1.5, 2.9)], color='#B91C1C', lw=1.8,
            label="Continuous Feedback & Optimization Loop", l_pos=(6.5, 1.6))
save(fig, 'fig05_sdlc_model.png')

# ==============================================================================
# FIG 6: System Architecture (5 Layers, already tested clean)
# ==============================================================================
# Already tested in generate_clean_core.py, re-running to keep in master script
fig, ax = new_canvas(14.0, 8.2)
layers_def = [
    (7.0, 1.5, "PRESENTATION LAYER  (User Interface & Visualization)", '#1E3A8A', '#F8FAFC'),
    (5.2, 1.5, "APPLICATION & API GATEWAY LAYER  (FastAPI Framework)", '#065F46', '#F8FAFC'),
    (3.4, 1.5, "INTELLIGENCE CORE  (Machine Learning & Optimization)", '#4338CA', '#F8FAFC'),
    (1.4, 1.8, "PERSISTENCE & DATA ACCESS LAYER  (Storage & Integrity)", '#334155', '#F8FAFC'),
]
for yc, h, label, b_col, bg_col in layers_def:
    rect = FancyBboxPatch((0.5, yc - h/2), 13.0, h, boxstyle="round,pad=0.1",
                          linewidth=1.2, edgecolor=b_col, facecolor=bg_col, zorder=1)
    ax.add_patch(rect)
    header_w = 7.0
    hdr = FancyBboxPatch((0.7, yc + h/2 - 0.35), header_w, 0.32, boxstyle="square,pad=0.04",
                         linewidth=0, facecolor=b_col, zorder=2)
    ax.add_patch(hdr)
    ax.text(0.85, yc + h/2 - 0.19, label, ha='left', va='center',
            fontsize=8.5, fontweight='bold', color='#FFFFFF', fontfamily=FONT, zorder=3)

card(ax, 3.8, 6.7, 5.0, 0.8, "MR Daily Execution Portal", "Leaflet Map · Stop Checklist · Visit Logging", '#1E3A8A', '#EFF6FF', t_size=9, s_size=7.5)
card(ax, 10.2, 6.7, 5.0, 0.8, "Manager Performance Dashboard", "Territory Overview · Compliance KPI · Route Analytics", '#1E3A8A', '#EFF6FF', t_size=9, s_size=7.5)

card(ax, 2.7, 4.9, 3.2, 0.8, "REST API Endpoints", "/routes, /visits, /doctors", '#065F46', '#ECFDF5', t_size=8.5, s_size=7.2)
card(ax, 7.0, 4.9, 3.6, 0.8, "JWT Security & RBAC", "Role Claims & Token Interceptor", '#065F46', '#ECFDF5', t_size=8.5, s_size=7.2)
card(ax, 11.3, 4.9, 3.2, 0.8, "Service Orchestrator", "Dispatches ML & VRPTW Tasks", '#065F46', '#ECFDF5', t_size=8.5, s_size=7.2)

card(ax, 3.8, 3.1, 5.2, 0.9, "ML Priority Engine (scikit-learn)",
     "Random Forest Classifier  ·  Feature Engineering Pipeline\nClassifies Visit Importance: High / Medium / Low",
     '#92400E', '#FEF3C7', t_col='#78350F', t_size=9, s_size=7.5)
card(ax, 10.2, 3.1, 5.2, 0.9, "Route Optimizer (Google OR-Tools)",
     "VRPTW Formulation  ·  Distance-Time Matrix Solver\nConstraints: Time Windows, Service Durations, Max Shift",
     '#4338CA', '#EDE9FE', t_col='#3730A3', t_size=9, s_size=7.5)

card(ax, 3.8, 1.2, 5.2, 0.9, "Relational Database (PostgreSQL / Supabase)",
     "Doctors, Appointments, Visit Logs, User Roles\nOptimized Geolocation Indexing",
     '#334155', '#F1F5F9', t_size=9, s_size=7.5)
card(ax, 10.2, 1.2, 5.2, 0.9, "Route Plans & Travel Distance Cache",
     "Generated Daily Itineraries  ·  Precomputed Matrices\nHistorical Route Performance Audit",
     '#334155', '#F1F5F9', t_size=9, s_size=7.5)

arrow(ax, 3.8, 6.25, 3.8, 5.4, color='#1E3A8A', lw=1.5)
arrow(ax, 10.2, 6.25, 10.2, 5.4, color='#1E3A8A', lw=1.5)
arrow(ax, 3.8, 4.45, 3.8, 3.65, color='#065F46', lw=1.5)
arrow(ax, 10.2, 4.45, 10.2, 3.65, color='#065F46', lw=1.5)
arrow(ax, 3.8, 2.55, 3.8, 1.75, color='#4338CA', lw=1.5)
arrow(ax, 10.2, 2.55, 10.2, 1.75, color='#4338CA', lw=1.5)
save(fig, 'fig06_architecture.png')

# ==============================================================================
# FIG 7: End-to-End MR Data Flow
# ==============================================================================
fig, ax = new_canvas(14.0, 6.0)
f7_row1 = [
    (1.6, 4.5, 2.2, 1.1, "1. MR Login", "JWT Authentication", '#1E3A8A', '#EFF6FF'),
    (4.4, 4.5, 2.4, 1.1, "2. Select Date & Territory", "Daily operational scope", '#0369A1', '#F0F9FF'),
    (7.5, 4.5, 2.6, 1.1, "3. Query Doctors & Appts", "Fetch candidate doctors", '#065F46', '#ECFDF5'),
    (10.8, 4.5, 2.6, 1.1, "4. Feature Engineering", "Calculate recency & trends", '#92400E', '#FEF3C7'),
]
for x, y, w, h, t, s, b, f in f7_row1:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=8.8, s_size=7.5)

arrow(ax, 2.8, 4.5, 3.1, 4.5)
arrow(ax, 5.7, 4.5, 6.1, 4.5)
arrow(ax, 8.9, 4.5, 9.4, 4.5)

ortho_arrow(ax, [(12.2, 4.5), (12.8, 4.5), (12.8, 1.8), (12.2, 1.8)])

f7_row2 = [
    (10.8, 1.8, 2.6, 1.1, "5. ML Priority Scoring", "Random Forest classifier", '#4338CA', '#EDE9FE'),
    (7.5, 1.8, 2.6, 1.1, "6. VRPTW Optimizer", "OR-Tools schedule solver", '#0D9488', '#F0FDFA'),
    (4.4, 1.8, 2.4, 1.1, "7. Generate Route Plan", "Turn-by-turn itinerary", '#B91C1C', '#FEF2F2'),
    (1.6, 1.8, 2.2, 1.1, "8. Map Dashboard", "Interactive Leaflet UI", '#1E3A8A', '#EFF6FF'),
]
for x, y, w, h, t, s, b, f in f7_row2:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=8.8, s_size=7.5)

arrow(ax, 9.4, 1.8, 8.9, 1.8)
arrow(ax, 6.1, 1.8, 5.7, 1.8)
arrow(ax, 3.1, 1.8, 2.8, 1.8)
save(fig, 'fig07_data_flow.png')

# ==============================================================================
# FIG 8: Use Case UML Diagram (Clean, actor outside boundary box)
# ==============================================================================
fig, ax = new_canvas(14.0, 7.8)
bx, by, bw, bh = 3.2, 0.4, 7.6, 6.8
boundary = FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.15",
                          linewidth=1.8, edgecolor='#1E3A8A', facecolor='#F8FAFC', zorder=1)
ax.add_patch(boundary)
ax.text(bx + bw/2, by + bh - 0.4, "MR Visit Prioritization & Route Optimization System",
        ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1E3A8A', fontfamily=FONT, zorder=2)
ax.plot([bx + 0.5, bx + bw - 0.5], [by + bh - 0.65, by + bh - 0.65], color='#CBD5E1', lw=1.0, zorder=2)

def draw_uml_actor(ax, x, y, name):
    c = Circle((x, y + 0.45), 0.22, facecolor='#FFFFFF', edgecolor='#1E293B', lw=1.8, zorder=4)
    ax.add_patch(c)
    ax.plot([x, x], [y + 0.23, y - 0.25], color='#1E293B', lw=2.0, zorder=4)
    ax.plot([x - 0.35, x + 0.35], [y + 0.08, y + 0.08], color='#1E293B', lw=2.0, zorder=4)
    ax.plot([x, x - 0.3], [y - 0.25, y - 0.7], color='#1E293B', lw=2.0, zorder=4)
    ax.plot([x, x + 0.3], [y - 0.25, y - 0.7], color='#1E293B', lw=2.0, zorder=4)
    ax.text(x, y - 1.0, name, ha='center', va='center', fontsize=9.0, fontweight='bold',
            color='#0F172A', fontfamily=FONT, multialignment='center', zorder=4)

draw_uml_actor(ax, 1.5, 3.8, "Medical\nRepresentative\n(MR)")
draw_uml_actor(ax, 12.5, 3.8, "Field Sales\nManager")

use_cases_list = [
    (5.0, 5.5, "Authenticate & Sign In", 'both'),
    (5.0, 4.4, "View Today's Assigned Visits", 'mr'),
    (5.0, 3.3, "Request Route Optimization", 'mr'),
    (5.0, 2.2, "Log Visit & Outcomes", 'mr'),
    (5.0, 1.1, "View Route on Map", 'mr'),
    (9.0, 4.4, "Manage Doctors & Territories", 'manager'),
    (9.0, 3.3, "Monitor Field Team Progress", 'manager'),
    (9.0, 2.2, "Review Route Analytics & KPIs", 'manager'),
    (9.0, 1.1, "Export Audit & Compliance Logs", 'manager'),
]
for cx, cy, text, role in use_cases_list:
    ellipse = mpatches.Ellipse((cx, cy), 3.2, 0.72, edgecolor='#1E3A8A', facecolor='#FFFFFF', lw=1.4, zorder=3)
    ax.add_patch(ellipse)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=8.2, fontweight='bold',
            color='#1E293B', fontfamily=FONT, multialignment='center', zorder=4)
    if role in ('mr', 'both'):
        ax.plot([1.9, cx - 1.6], [3.8, cy], color='#64748B', lw=1.1, zorder=2)
    if role in ('manager', 'both'):
        ax.plot([12.1, cx + 1.6], [3.8, cy], color='#64748B', lw=1.1, zorder=2)

save(fig, 'fig08_use_case.png')

# ==============================================================================
# FIG 9: Activity UML Diagram (MR Daily Execution Flow)
# ==============================================================================
fig, ax = new_canvas(14.0, 7.0)
c_start = Circle((1.2, 5.5), 0.22, facecolor='#0F172A', edgecolor='#0F172A', zorder=3)
ax.add_patch(c_start)
ax.text(1.2, 5.95, "Start", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

card(ax, 3.4, 5.5, 2.2, 0.8, "Sign In & Auth", "Validate Token", '#1E3A8A', '#EFF6FF', t_size=8.5)
arrow(ax, 1.45, 5.5, 2.2, 5.5)

card(ax, 6.6, 5.5, 2.4, 0.8, "Fetch Today's Schedule", "Candidate Doctors", '#065F46', '#ECFDF5', t_size=8.5)
arrow(ax, 4.6, 5.5, 5.3, 5.5)

card(ax, 10.2, 5.5, 2.8, 0.8, "Generate Optimized Route", "Run ML & OR-Tools", '#4338CA', '#EDE9FE', t_size=8.5)
arrow(ax, 7.9, 5.5, 8.7, 5.5)

card(ax, 10.2, 3.8, 2.8, 0.8, "Travel to Stop Location", "Navigate Turn-by-Turn", '#0369A1', '#F0F9FF', t_size=8.5)
arrow(ax, 10.2, 5.0, 10.2, 4.3)

# Doctor available diamond
d = Polygon([(6.6, 4.1), (7.4, 3.8), (6.6, 3.5), (5.8, 3.8)], closed=True,
            edgecolor='#0F172A', facecolor='#FEF3C7', lw=1.5, zorder=3)
ax.add_patch(d)
ax.text(6.6, 3.8, "Doctor\nAvailable?", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A', zorder=4)
arrow(ax, 8.7, 3.8, 7.5, 3.8)

card(ax, 6.6, 2.0, 2.4, 0.8, "Conduct Consultation", "Log Detailing Notes", '#065F46', '#ECFDF5', t_size=8.5)
arrow(ax, 6.6, 3.45, 6.6, 2.5, label="[Yes]")

card(ax, 3.4, 3.8, 2.2, 0.8, "Log Missed / Delay", "Record Reason", '#B91C1C', '#FEF2F2', t_size=8.5)
arrow(ax, 5.75, 3.8, 4.6, 3.8, label="[No]", label_above=True)

# More stops diamond
d2 = Polygon([(3.4, 2.3), (4.2, 2.0), (3.4, 1.7), (2.6, 2.0)], closed=True,
             edgecolor='#0F172A', facecolor='#FEF3C7', lw=1.5, zorder=3)
ax.add_patch(d2)
ax.text(3.4, 2.0, "More\nStops?", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A', zorder=4)
arrow(ax, 5.3, 2.0, 4.3, 2.0)
arrow(ax, 3.4, 3.3, 3.4, 2.4)

ortho_arrow(ax, [(3.4, 1.65), (3.4, 0.8), (10.2, 0.8), (10.2, 3.3)], color='#0284C7', lw=1.5,
            label="[Yes - Next Stop]", l_pos=(6.8, 0.6))

c_end_outer = Circle((1.2, 2.0), 0.24, edgecolor='#0F172A', facecolor='#FFFFFF', lw=2, zorder=3)
c_end_inner = Circle((1.2, 2.0), 0.14, edgecolor='#0F172A', facecolor='#0F172A', zorder=4)
ax.add_patch(c_end_outer)
ax.add_patch(c_end_inner)
ax.text(1.2, 2.45, "End Day", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')
arrow(ax, 2.55, 2.0, 1.5, 2.0, label="[No]")
save(fig, 'fig09_activity_mr.png')

# ==============================================================================
# FIG 10: Sequence Diagram (Already tested clean)
# ==============================================================================
fig, ax = new_canvas(14.0, 8.0)
lifelines = [
    (1.4, "MR Actor", '#1E3A8A'),
    (3.8, "React Frontend", '#0284C7'),
    (6.4, "FastAPI Gateway", '#065F46'),
    (9.0, "Database (Supabase)", '#334155'),
    (11.2, "ML Priority Model", '#92400E'),
    (13.0, "OR-Tools Solver", '#4338CA'),
]
for lx, name, col in lifelines:
    card(ax, lx, 7.3, 2.0, 0.6, name, None, border=col, fill=col+'15', t_col=col, t_size=8.2)
    ax.plot([lx, lx], [6.9, 0.6], color='#94A3B8', lw=1.2, ls='--', zorder=1)

messages = [
    (1.4, 3.8, 6.4, "1. Click 'Generate Optimized Route'", False, '#1E3A8A'),
    (3.8, 6.4, 5.8, "2. POST /api/routes/generate", False, '#0284C7'),
    (6.4, 9.0, 5.2, "3. Query doctors & availability slots", False, '#065F46'),
    (9.0, 6.4, 4.6, "4. Return doctor records & GPS coords", True, '#065F46'),
    (6.4, 11.2, 4.0, "5. predict_priority(features)", False, '#92400E'),
    (11.2, 6.4, 3.4, "6. Return priority classes [H / M / L]", True, '#92400E'),
    (6.4, 13.0, 2.8, "7. solve_vrptw(distance_matrix, windows)", False, '#4338CA'),
    (13.0, 6.4, 2.2, "8. Return optimal sequence & ETAs", True, '#4338CA'),
    (6.4, 9.0, 1.6, "9. Persist route plan & stops to DB", False, '#334155'),
    (6.4, 3.8, 1.0, "10. Return route JSON payload", True, '#0284C7'),
]
for x1, x2, y, text, is_ret, col in messages:
    ls = '--' if is_ret else '-'
    arrow_style = '-|>' if not is_ret else '->'
    a = FancyArrowPatch((x1, y), (x2, y), arrowstyle=arrow_style, mutation_scale=13,
                        linewidth=1.4, color=col, linestyle=ls, zorder=3)
    ax.add_patch(a)
    mx = (x1 + x2) / 2
    ax.text(mx, y + 0.16, text, ha='center', va='center', fontsize=7.8,
            fontweight='bold', color=col, fontfamily=FONT, zorder=4,
            bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none'))
save(fig, 'fig10_sequence_diagram.png')

# ==============================================================================
# FIG 11: Conceptual UML Class Diagram (Formal 3-compartment boxes)
# ==============================================================================
fig, ax = new_canvas(14.0, 7.5)

def uml_class(ax, x, y, w, h, name, attrs, methods, col='#1E3A8A'):
    # Outer box
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.04",
                       linewidth=1.4, edgecolor=col, facecolor='#FFFFFF', zorder=2)
    ax.add_patch(p)
    # Header compartment
    hh = 0.52
    hp = Rectangle((x - w/2, y + h/2 - hh), w, hh, facecolor=col + '18', edgecolor='none', zorder=2)
    ax.add_patch(hp)
    ax.text(x, y + h/2 - 0.26, name, ha='center', va='center', fontsize=9.0, fontweight='bold', color=col, zorder=3)
    ax.plot([x - w/2, x + w/2], [y + h/2 - hh, y + h/2 - hh], color=col, lw=1.2, zorder=3)
    # Attributes
    ay = y + h/2 - hh - 0.22
    for a in attrs:
        ax.text(x - w/2 + 0.12, ay, f"+ {a}", ha='left', va='center', fontsize=7.5, color='#334155', fontfamily=FONT, zorder=3)
        ay -= 0.24
    # Divider
    div_y = y - h/2 + len(methods)*0.24 + 0.18
    ax.plot([x - w/2, x + w/2], [div_y, div_y], color=col, lw=0.9, ls='--', zorder=3)
    # Methods
    my = div_y - 0.20
    for m in methods:
        ax.text(x - w/2 + 0.12, my, f"+ {m}()", ha='left', va='center', fontsize=7.5, color=col, fontweight='semibold', fontfamily=FONT, zorder=3)
        my -= 0.24

uml_class(ax, 1.8, 5.4, 2.6, 2.1, "User", ["user_id: int", "email: string", "role: string"], ["login()", "validate_token()"], '#1E3A8A')
uml_class(ax, 5.2, 5.4, 3.0, 2.1, "MedicalRep", ["mr_id: int", "territory: string", "max_hours: float"], ["request_route()", "get_status()"], '#065F46')
uml_class(ax, 8.8, 5.4, 3.0, 2.1, "Doctor", ["doctor_id: int", "specialty: string", "lat, lon: float"], ["get_schedule()"], '#92400E')
uml_class(ax, 12.2, 5.4, 2.6, 2.1, "PriorityPrediction", ["pred_id: int", "score: float", "class: string"], ["predict()", "explain()"], '#4338CA')

uml_class(ax, 3.5, 2.0, 3.2, 2.1, "Route", ["route_id: int", "mr_id: int", "date: date", "total_dist_km: float"], ["optimize()", "export()"], '#0D9488')
uml_class(ax, 7.4, 2.0, 3.2, 2.1, "RouteStop", ["stop_id: int", "route_id: int", "seq: int", "eta, etd: time"], ["mark_visited()"], '#B91C1C')
uml_class(ax, 11.2, 2.0, 2.8, 2.1, "VisitRecord", ["visit_id: int", "status: string", "notes: text"], ["complete()", "reschedule()"], '#334155')

ax.plot([3.1, 3.7], [5.4, 5.4], color='#64748B', lw=1.2)
ax.plot([6.7, 7.3], [5.4, 5.4], color='#64748B', lw=1.2)
ax.plot([10.3, 10.9], [5.4, 5.4], color='#64748B', lw=1.2)
ax.plot([5.1, 5.8], [2.0, 2.0], color='#64748B', lw=1.2)
ax.plot([9.0, 9.8], [2.0, 2.0], color='#64748B', lw=1.2)
ax.plot([5.2, 3.5], [4.3, 3.1], color='#64748B', lw=1.2)
ax.plot([8.8, 7.4], [4.3, 3.1], color='#64748B', lw=1.2)
save(fig, 'fig11_class_diagram.png')

# ==============================================================================
# FIG 12: Entity-Relationship (ER) Diagram
# ==============================================================================
fig, ax = new_canvas(14.0, 7.2)

def er_table(ax, x, y, w, h, name, fields, col='#1E3A8A'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.04",
                       linewidth=1.4, edgecolor=col, facecolor='#FFFFFF', zorder=2)
    ax.add_patch(p)
    hh = 0.48
    hp = Rectangle((x - w/2, y + h/2 - hh), w, hh, facecolor=col + '20', edgecolor='none', zorder=2)
    ax.add_patch(hp)
    ax.text(x, y + h/2 - 0.24, name, ha='center', va='center', fontsize=8.8, fontweight='bold', color=col, zorder=3)
    ax.plot([x - w/2, x + w/2], [y + h/2 - hh, y + h/2 - hh], color=col, lw=1.2, zorder=3)
    
    fy = y + h/2 - hh - 0.22
    for f in fields:
        is_key = f.startswith('PK') or f.startswith('FK')
        clr = col if is_key else '#475569'
        weight = 'bold' if is_key else 'normal'
        ax.text(x - w/2 + 0.12, fy, f, ha='left', va='center', fontsize=7.4, color=clr, fontweight=weight, zorder=3)
        fy -= 0.24

er_table(ax, 1.8, 5.2, 2.6, 2.2, "USERS", ["PK user_id", "email VARCHAR", "password_hash", "role ENUM", "created_at"], '#1E3A8A')
er_table(ax, 5.4, 5.2, 2.8, 2.2, "MEDICAL_REPS", ["PK mr_id", "FK user_id", "territory VARCHAR", "start_lat, lon", "work_hours_limit"], '#065F46')
er_table(ax, 9.2, 5.2, 2.8, 2.4, "DOCTORS", ["PK doctor_id", "name VARCHAR", "specialization", "lat, lon DECIMAL", "avail_start, end", "avg_duration_min"], '#92400E')
er_table(ax, 12.3, 5.2, 2.4, 2.0, "PREDICTIONS", ["PK pred_id", "FK doctor_id", "priority_score", "priority_level", "model_version"], '#4338CA')

er_table(ax, 3.6, 1.8, 2.8, 2.2, "ROUTES", ["PK route_id", "FK mr_id", "plan_date DATE", "total_distance_km", "total_duration_min", "status VARCHAR"], '#0D9488')
er_table(ax, 7.6, 1.8, 3.0, 2.4, "ROUTE_STOPS", ["PK stop_id", "FK route_id", "FK doctor_id", "sequence_order INT", "est_arrival TIME", "est_departure TIME", "status ENUM"], '#B91C1C')
er_table(ax, 11.4, 1.8, 2.6, 2.0, "VISIT_LOGS", ["PK visit_id", "FK doctor_id", "FK mr_id", "visit_date DATE", "outcome VARCHAR"], '#334155')

def er_rel(ax, x1, y1, x2, y2, label):
    ax.plot([x1, x2], [y1, y2], color='#64748B', lw=1.2, zorder=2)
    mx, my = (x1 + x2)/2, (y1 + y2)/2
    ax.text(mx, my, label, ha='center', va='center', fontsize=7.2, color='#0F172A',
            fontweight='bold', bbox=dict(boxstyle='square,pad=0.1', facecolor='#F1F5F9', edgecolor='none'), zorder=3)

er_rel(ax, 3.1, 5.2, 4.0, 5.2, "1 : 1")
er_rel(ax, 6.8, 5.2, 7.8, 5.2, "1 : N")
er_rel(ax, 10.6, 5.2, 11.1, 5.2, "1 : N")
er_rel(ax, 5.0, 1.8, 6.1, 1.8, "1 : N")
er_rel(ax, 9.1, 1.8, 10.1, 1.8, "1 : N")
er_rel(ax, 5.4, 4.0, 3.6, 2.9, "1 : N")
er_rel(ax, 9.2, 3.9, 7.6, 3.0, "1 : N")
save(fig, 'fig12_er_diagram.png')

# ==============================================================================
# FIG 13: State Machine Diagram (Route Lifecycle)
# ==============================================================================
fig, ax = new_canvas(14.0, 5.4)
c13_start = Circle((1.0, 3.6), 0.2, facecolor='#0F172A', edgecolor='#0F172A', zorder=3)
ax.add_patch(c13_start)

card(ax, 2.8, 3.6, 2.2, 1.0, "Draft Request", "Target input selected", '#1E3A8A', '#EFF6FF', t_size=8.5)
arrow(ax, 1.2, 3.6, 1.7, 3.6)

card(ax, 5.8, 3.6, 2.2, 1.0, "Validated", "Constraints satisfied", '#065F46', '#ECFDF5', t_size=8.5)
arrow(ax, 3.9, 3.6, 4.7, 3.6, label="Valid Constraints")

card(ax, 9.0, 3.6, 2.4, 1.0, "Optimized / Scheduled", "VRPTW Solver solved", '#4338CA', '#EDE9FE', t_size=8.5)
arrow(ax, 6.9, 3.6, 7.8, 3.6, label="Solve Route")

card(ax, 12.0, 3.6, 2.0, 1.0, "In Progress", "MR en route", '#0D9488', '#F0FDFA', t_size=8.5)
arrow(ax, 10.2, 3.6, 11.0, 3.6, label="Start Day")

card(ax, 5.8, 1.4, 2.2, 0.9, "Validation Failed", "Conflict detected", '#B91C1C', '#FEF2F2', t_size=8)
ortho_arrow(ax, [(2.8, 3.1), (2.8, 1.4), (4.7, 1.4)], label="[Invalid]", color='#B91C1C', l_pos=(3.6, 1.6))
ortho_arrow(ax, [(5.8, 1.85), (5.8, 2.5), (3.9, 2.5), (3.9, 3.1)], label="[Fix Params]", color='#0284C7', l_pos=(4.8, 2.7))

card(ax, 12.0, 1.4, 2.0, 0.9, "Completed", "All visits executed", '#065F46', '#ECFDF5', t_size=8.5)
arrow(ax, 12.0, 3.1, 12.0, 1.85, label="All Stops Done")

c13_end_outer = Circle((9.5, 1.4), 0.22, edgecolor='#0F172A', facecolor='#FFFFFF', lw=2, zorder=3)
c13_end_inner = Circle((9.5, 1.4), 0.13, edgecolor='#0F172A', facecolor='#0F172A', zorder=4)
ax.add_patch(c13_end_outer)
ax.add_patch(c13_end_inner)
arrow(ax, 11.0, 1.4, 9.8, 1.4)
save(fig, 'fig13_state_diagram.png')

# ==============================================================================
# FIG 14: Component Diagram
# ==============================================================================
fig, ax = new_canvas(14.0, 6.5)

def comp_box(ax, x, y, w, h, name, sub, col='#1E3A8A', fill='#EFF6FF'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                       linewidth=1.4, edgecolor=col, facecolor=fill, zorder=2)
    ax.add_patch(p)
    # 2 small tab rectangles on top-left of component
    tab1 = Rectangle((x - w/2 - 0.18, y + h*0.12), 0.36, 0.20, facecolor=fill, edgecolor=col, lw=1.2, zorder=3)
    tab2 = Rectangle((x - w/2 - 0.18, y - h*0.32), 0.36, 0.20, facecolor=fill, edgecolor=col, lw=1.2, zorder=3)
    ax.add_patch(tab1)
    ax.add_patch(tab2)
    ax.text(x, y + 0.16, name, ha='center', va='center', fontsize=9.0, fontweight='bold', color=col, zorder=4)
    ax.text(x, y - 0.22, sub, ha='center', va='center', fontsize=7.6, color='#475569', zorder=4)

comp_box(ax, 2.2, 3.5, 3.4, 1.6, "React Web Application", "UI Components & Leaflet Maps", '#1E3A8A', '#EFF6FF')
comp_box(ax, 6.6, 3.5, 3.4, 1.6, "FastAPI REST Server", "Gateway, Security & Controllers", '#065F46', '#ECFDF5')
comp_box(ax, 11.4, 5.2, 3.2, 1.4, "ML Priority Engine", "Random Forest Microservice", '#92400E', '#FEF3C7')
comp_box(ax, 11.4, 3.5, 3.2, 1.4, "Route Optimizer", "Google OR-Tools VRPTW", '#4338CA', '#EDE9FE')
comp_box(ax, 11.4, 1.8, 3.2, 1.4, "Persistence Module", "Supabase PostgreSQL ORM", '#334155', '#F1F5F9')

arrow(ax, 3.9, 3.5, 4.9, 3.5, label="REST / JSON")
ortho_arrow(ax, [(8.3, 3.8), (9.2, 3.8), (9.2, 5.2), (9.8, 5.2)], label="predict()")
arrow(ax, 8.3, 3.5, 9.8, 3.5, label="solve_vrptw()")
ortho_arrow(ax, [(8.3, 3.2), (9.2, 3.2), (9.2, 1.8), (9.8, 1.8)], label="ORM Queries")
save(fig, 'fig14_component_diagram.png')

# ==============================================================================
# FIG 15: Deployment Diagram
# ==============================================================================
fig, ax = new_canvas(14.0, 6.0)

def deploy_node(ax, x, y, w, h, name, sub, col='#1E3A8A', fill='#F8FAFC'):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                       linewidth=1.4, edgecolor=col, facecolor=fill, zorder=2)
    ax.add_patch(p)
    ax.text(x, y + h*0.28, "<<device / node>>", ha='center', va='center', fontsize=7.5, color='#64748B', zorder=3)
    ax.text(x, y + 0.06, name, ha='center', va='center', fontsize=9.2, fontweight='bold', color=col, zorder=3)
    ax.text(x, y - h*0.26, sub, ha='center', va='center', fontsize=7.8, color='#475569', zorder=3)

deploy_node(ax, 2.2, 3.0, 3.4, 2.2, "Client Browser\n(Desktop / Mobile)", "React SPA on Vercel Edge\nHTTPS / TLS 1.3", '#1E3A8A', '#EFF6FF')
deploy_node(ax, 6.8, 3.0, 3.6, 2.2, "FastAPI Application Server\n(Cloud Container / VM)", "Python 3.12 + Uvicorn ASGI\nOR-Tools + scikit-learn", '#065F46', '#ECFDF5')
deploy_node(ax, 11.4, 4.5, 3.4, 1.8, "Database Server\n(Supabase Cloud)", "PostgreSQL 15+ Managed Instance\nSSL Connection (Port 5432)", '#334155', '#F1F5F9')
deploy_node(ax, 11.4, 1.8, 3.4, 1.8, "Routing Matrix API\n(OSRM / Maps API)", "Distance & Duration Engine\nHTTPS REST Service", '#4338CA', '#EDE9FE')

arrow(ax, 3.9, 3.0, 5.0, 3.0, label="HTTPS REST")
ortho_arrow(ax, [(8.6, 3.5), (9.2, 3.5), (9.2, 4.5), (9.7, 4.5)], label="TCP / SSL")
ortho_arrow(ax, [(8.6, 2.5), (9.2, 2.5), (9.2, 1.8), (9.7, 1.8)], label="HTTPS")
save(fig, 'fig15_deployment_diagram.png')

# ==============================================================================
# FIG 16: Priority Prediction ML Pipeline
# ==============================================================================
fig, ax = new_canvas(14.0, 5.4)
f16_nodes = [
    (1.5, 3.0, 2.2, 1.4, "1. Raw Visit Data", "Doctor visit histories\nPrior outcomes & notes", '#1E3A8A', '#EFF6FF'),
    (4.1, 3.0, 2.2, 1.4, "2. Preprocessing", "Missing value imputation\nCategorical encoding", '#0369A1', '#F0F9FF'),
    (6.8, 3.0, 2.4, 1.4, "3. Feature Pipeline", "Days elapsed, frequency\nStrategic tier & target tier", '#065F46', '#ECFDF5'),
    (9.6, 3.0, 2.4, 1.4, "4. Model Training", "Random Forest Classifier\nHyperparameter tuning", '#92400E', '#FEF3C7'),
    (12.3, 3.0, 2.2, 1.4, "5. Priority Classes", "High / Medium / Low\nCalibrated probability", '#4338CA', '#EDE9FE'),
]
for x, y, w, h, t, s, b, f in f16_nodes:
    card(ax, x, y, w, h, t, s, border=b, fill=f, t_size=8.8, s_size=7.5)

arrow(ax, 2.6, 3.0, 3.0, 3.0)
arrow(ax, 5.2, 3.0, 5.6, 3.0)
arrow(ax, 8.0, 3.0, 8.4, 3.0)
arrow(ax, 10.8, 3.0, 11.2, 3.0)
save(fig, 'fig16_ml_pipeline.png')

print("All 16 diagrams generated with high precision!")
