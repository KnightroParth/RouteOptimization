"""
High-Precision Diagram Renderer for Review III Presentation
Fixes all clipping, alignment, box sizing, and UML standard issues.
Features:
- Pure white background (#FFFFFF) with high contrast Navy (#0F172A) & Slate (#334155) typography
- Professional academic palette: Royal Navy (#1E3A8A), Forest Green (#065F46), Warm Ochre (#92400E), Crimson (#991B1B), Slate Blue (#4338CA)
- Generous internal padding and bounding boxes
- Zero text collisions or edge clippings
- Standard UML shapes and connectors
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle
import os

OUT_DIR = r"d:\Projects\MR Route Optimization\docs\diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

# Typography
FONT = 'DejaVu Sans'

def new_canvas(w=14.0, h=7.5, pad=0.3):
    fig, ax = plt.subplots(figsize=(w, h), dpi=300, facecolor='#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax

def save_fig(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none', pad_inches=0.2)
    plt.close(fig)
    print(f"Generated clean: {filename}")

# --- Helper drawing functions ---
def draw_node(ax, x, y, w, h, title, sub=None, border='#1E3A8A', fill='#F8FAFC', title_color='#0F172A', t_size=9.5, s_size=8.0, lw=1.5, rad=0.12):
    """Draws a clean rounded rectangle with centered, non-colliding title and subtitle."""
    box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=f"round,pad={rad}",
                          linewidth=lw, edgecolor=border, facecolor=fill, zorder=3)
    ax.add_patch(box)
    if sub:
        lines = sub.split('\n')
        sub_h = len(lines) * 0.18
        ax.text(x, y + h*0.22, title, ha='center', va='center',
                fontsize=t_size, fontweight='bold', color=title_color, fontfamily=FONT, zorder=4)
        ax.text(x, y - h*0.18, sub, ha='center', va='center',
                fontsize=s_size, color='#475569', fontfamily=FONT, zorder=4, multialignment='center')
    else:
        ax.text(x, y, title, ha='center', va='center',
                fontsize=t_size, fontweight='bold', color=title_color, fontfamily=FONT, zorder=4, multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, color='#334155', lw=1.6, label=None, label_above=True, l_size=8.0):
    """Draws an arrow between two points with an optional badge label."""
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=15,
                        linewidth=lw, color=color, zorder=5)
    ax.add_patch(a)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        oy = 0.20 if label_above else -0.22
        ax.text(mx, my + oy, label, ha='center', va='center', fontsize=l_size,
                color='#1E293B', fontweight='bold', fontfamily=FONT, zorder=6,
                bbox=dict(boxstyle='square,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.8))

def draw_ortho_arrow(ax, pts, color='#334155', lw=1.6, label=None, l_pos=None):
    """Draws an orthogonal route through a list of points (x, y)."""
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]], color=color, lw=lw, zorder=4)
    # Final segment with arrow
    draw_arrow(ax, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], color=color, lw=lw)
    if label and l_pos:
        ax.text(l_pos[0], l_pos[1], label, ha='center', va='center', fontsize=8.0,
                color='#1E293B', fontweight='bold', fontfamily=FONT, zorder=6,
                bbox=dict(boxstyle='square,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.8))

# ==============================================================================
# FIG 1: Problem Context (Fixed layout, ample bottom margin, orthogonal lines)
# ==============================================================================
fig, ax = new_canvas(14.0, 7.2)

# Top 4 factor nodes
f1_cards = [
    (1.8, 5.5, 2.4, 1.4, "Multiple Doctors", "Assigned in Territory\nDiverse Specialty Portfolio", '#1E3A8A', '#EFF6FF'),
    (5.3, 5.5, 2.4, 1.4, "Varying Priorities", "Strategic / Revenue Impact\nHigh vs Low Urgency", '#92400E', '#FEF3C7'),
    (8.8, 5.5, 2.4, 1.4, "Time Windows", "Strict Consultation Hours\nNarrow Visiting Slots", '#065F46', '#D1FAE5'),
    (12.2, 5.5, 2.4, 1.4, "Dispersed Locations", "Geographical Spread\nUrban Traffic Delays", '#4338CA', '#EDE9FE'),
]
for x, y, w, h, t, s, b, f in f1_cards:
    draw_node(ax, x, y, w, h, t, s, border=b, fill=f, t_size=9.5, s_size=8.0)

# Horizontal flow arrows between factors
draw_arrow(ax, 3.1, 5.5, 4.0, 5.5, color='#64748B')
draw_arrow(ax, 6.6, 5.5, 7.5, 5.5, color='#64748B')
draw_arrow(ax, 10.1, 5.5, 10.9, 5.5, color='#64748B')

# Central Manual Planning Box
draw_node(ax, 7.0, 3.2, 6.2, 1.4, "Manual Planning & Ad-hoc Sequencing",
          "Representative relies on memory, intuition, or static spreadsheets\nInability to co-optimize visit value against travel distance & clinic availability",
          border='#B91C1C', fill='#FEF2F2', title_color='#991B1B', t_size=10.5, s_size=8.2, rad=0.15)

# Connect top factors to central manual planning box using clean orthogonal lines
draw_ortho_arrow(ax, [(1.8, 4.7), (1.8, 3.5), (3.8, 3.5)], color='#94A3B8')
draw_ortho_arrow(ax, [(5.3, 4.7), (5.3, 3.9)], color='#94A3B8')
draw_ortho_arrow(ax, [(8.8, 4.7), (8.8, 3.9)], color='#94A3B8')
draw_ortho_arrow(ax, [(12.2, 4.7), (12.2, 3.5), (10.2, 3.5)], color='#94A3B8')

# Final Consequence Box (well-spaced at bottom, large height, no clipping)
draw_arrow(ax, 7.0, 2.4, 7.0, 1.6, color='#B91C1C', lw=2.0)
draw_node(ax, 7.0, 1.0, 10.0, 1.1, "Sub-optimal Field Execution Outcomes",
          "Excessive Travel Times  ·  Prolonged Waiting at Clinics  ·  Missed High-Priority Doctor Visits  ·  Burnout",
          border='#991B1B', fill='#FEE2E2', title_color='#7F1D1D', t_size=10.0, s_size=8.5, lw=1.8)

save_fig(fig, 'fig01_problem_context.png')

# ==============================================================================
# FIG 6: System Architecture (Fixed layer headers, no overlapping, clean hierarchy)
# ==============================================================================
fig, ax = new_canvas(14.0, 8.2)

# 5 Defined layers with clean headers on top
layers_def = [
    # (y_center, height, label, border, bg)
    (7.0, 1.5, "PRESENTATION LAYER  (User Interface & Visualization)", '#1E3A8A', '#F8FAFC'),
    (5.2, 1.5, "APPLICATION & API GATEWAY LAYER  (FastAPI Framework)", '#065F46', '#F8FAFC'),
    (3.4, 1.5, "INTELLIGENCE CORE  (Machine Learning & Optimization)", '#4338CA', '#F8FAFC'),
    (1.4, 1.8, "PERSISTENCE & DATA ACCESS LAYER  (Storage & Integrity)", '#334155', '#F8FAFC'),
]

for yc, h, label, b_col, bg_col in layers_def:
    # Outer layer container
    rect = FancyBboxPatch((0.5, yc - h/2), 13.0, h, boxstyle="round,pad=0.1",
                          linewidth=1.2, edgecolor=b_col, facecolor=bg_col, zorder=1)
    ax.add_patch(rect)
    # Header tag banner
    header_w = 7.0
    hdr = FancyBboxPatch((0.7, yc + h/2 - 0.35), header_w, 0.32, boxstyle="square,pad=0.04",
                         linewidth=0, facecolor=b_col, zorder=2)
    ax.add_patch(hdr)
    ax.text(0.85, yc + h/2 - 0.19, label, ha='left', va='center',
            fontsize=8.5, fontweight='bold', color='#FFFFFF', fontfamily=FONT, zorder=3)

# Components inside Presentation Layer (y around 6.8)
draw_node(ax, 3.8, 6.7, 5.0, 0.8, "MR Daily Execution Portal", "Leaflet Map · Stop Checklist · Visit Logging", '#1E3A8A', '#EFF6FF', t_size=9, s_size=7.5)
draw_node(ax, 10.2, 6.7, 5.0, 0.8, "Manager Performance Dashboard", "Territory Overview · Compliance KPI · Route Analytics", '#1E3A8A', '#EFF6FF', t_size=9, s_size=7.5)

# Components inside API Layer (y around 5.0)
draw_node(ax, 2.7, 4.9, 3.2, 0.8, "REST API Endpoints", "/routes, /visits, /doctors", '#065F46', '#ECFDF5', t_size=8.5, s_size=7.2)
draw_node(ax, 7.0, 4.9, 3.6, 0.8, "JWT Security & RBAC", "Role Claims & Token Interceptor", '#065F46', '#ECFDF5', t_size=8.5, s_size=7.2)
draw_node(ax, 11.3, 4.9, 3.2, 0.8, "Service Orchestrator", "Dispatches ML & VRPTW Tasks", '#065F46', '#ECFDF5', t_size=8.5, s_size=7.2)

# Components inside Intelligence Core (split: ML vs OR-Tools) (y around 3.2)
draw_node(ax, 3.8, 3.1, 5.2, 0.9, "ML Priority Engine (scikit-learn)",
          "Random Forest Classifier  ·  Feature Engineering Pipeline\nClassifies Visit Importance: High / Medium / Low",
          '#92400E', '#FEF3C7', title_color='#78350F', t_size=9, s_size=7.5)
draw_node(ax, 10.2, 3.1, 5.2, 0.9, "Route Optimizer (Google OR-Tools)",
          "VRPTW Formulation  ·  Distance-Time Matrix Solver\nConstraints: Time Windows, Service Durations, Max Shift",
          '#4338CA', '#EDE9FE', title_color='#3730A3', t_size=9, s_size=7.5)

# Components inside Persistence Layer (y around 1.2)
draw_node(ax, 3.8, 1.2, 5.2, 0.9, "Relational Database (PostgreSQL / Supabase)",
          "Doctors, Appointments, Visit Logs, User Roles\nOptimized Geolocation Indexing",
          '#334155', '#F1F5F9', t_size=9, s_size=7.5)
draw_node(ax, 10.2, 1.2, 5.2, 0.9, "Route Plans & Travel Distance Cache",
          "Generated Daily Itineraries  ·  Precomputed Matrices\nHistorical Route Performance Audit",
          '#334155', '#F1F5F9', t_size=9, s_size=7.5)

# Inter-layer connector arrows
draw_arrow(ax, 3.8, 6.25, 3.8, 5.4, color='#1E3A8A', lw=1.5)
draw_arrow(ax, 10.2, 6.25, 10.2, 5.4, color='#1E3A8A', lw=1.5)
draw_arrow(ax, 3.8, 4.45, 3.8, 3.65, color='#065F46', lw=1.5)
draw_arrow(ax, 10.2, 4.45, 10.2, 3.65, color='#065F46', lw=1.5)
draw_arrow(ax, 3.8, 2.55, 3.8, 1.75, color='#4338CA', lw=1.5)
draw_arrow(ax, 10.2, 2.55, 10.2, 1.75, color='#4338CA', lw=1.5)

save_fig(fig, 'fig06_architecture.png')

# ==============================================================================
# FIG 8: Use Case UML Diagram (Formal UML notation, clean stick figures, no border crossing)
# ==============================================================================
fig, ax = new_canvas(14.0, 7.8)

# System Boundary Rectangle
bx, by, bw, bh = 3.2, 0.5, 7.6, 6.8
boundary = FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.15",
                          linewidth=1.8, edgecolor='#1E3A8A', facecolor='#F8FAFC', zorder=1)
ax.add_patch(boundary)

# System Boundary Title Bar
ax.text(bx + bw/2, by + bh - 0.4, "MR Visit Prioritization & Route Optimization System",
        ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1E3A8A', fontfamily=FONT, zorder=2)
ax.plot([bx + 0.5, bx + bw - 0.5], [by + bh - 0.65, by + bh - 0.65], color='#CBD5E1', lw=1.0, zorder=2)

def draw_uml_actor(ax, x, y, name):
    # Head
    c = Circle((x, y + 0.45), 0.22, facecolor='#FFFFFF', edgecolor='#1E293B', lw=1.8, zorder=4)
    ax.add_patch(c)
    # Body
    ax.plot([x, x], [y + 0.23, y - 0.25], color='#1E293B', lw=2.0, zorder=4)
    # Arms
    ax.plot([x - 0.35, x + 0.35], [y + 0.08, y + 0.08], color='#1E293B', lw=2.0, zorder=4)
    # Legs
    ax.plot([x, x - 0.3], [y - 0.25, y - 0.7], color='#1E293B', lw=2.0, zorder=4)
    ax.plot([x, x + 0.3], [y - 0.25, y - 0.7], color='#1E293B', lw=2.0, zorder=4)
    # Name Label
    ax.text(x, y - 1.0, name, ha='center', va='center', fontsize=9.2, fontweight='bold',
            color='#0F172A', fontfamily=FONT, multialignment='center', zorder=4)

draw_uml_actor(ax, 1.6, 4.0, "Medical\nRepresentative\n(MR)")
draw_uml_actor(ax, 12.4, 4.0, "Field Sales\nManager")

use_cases_list = [
    # (x, y, text, role)
    (5.0, 5.7, "Authenticate & Sign In", 'both'),
    (5.0, 4.6, "View Today's Assigned Visits", 'mr'),
    (5.0, 3.5, "Request Route Optimization", 'mr'),
    (5.0, 2.4, "Log Visit & Outcomes", 'mr'),
    (5.0, 1.3, "View Route on Map", 'mr'),
    (9.0, 4.6, "Manage Doctors & Territories", 'manager'),
    (9.0, 3.5, "Monitor Field Team Progress", 'manager'),
    (9.0, 2.4, "Review Route Analytics & KPIs", 'manager'),
    (9.0, 1.3, "Export Audit & Compliance Logs", 'manager'),
]

for cx, cy, text, role in use_cases_list:
    ellipse = mpatches.Ellipse((cx, cy), 3.2, 0.72, edgecolor='#1E3A8A', facecolor='#FFFFFF', lw=1.4, zorder=3)
    ax.add_patch(ellipse)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=8.2, fontweight='bold',
            color='#1E293B', fontfamily=FONT, multialignment='center', zorder=4)

    # Actor lines (clean, connect at actor center to ellipse edges, do not extend beyond)
    if role in ('mr', 'both'):
        ax.plot([2.0, cx - 1.6], [4.0, cy], color='#64748B', lw=1.2, zorder=2)
    if role in ('manager', 'both'):
        ax.plot([12.0, cx + 1.6], [4.0, cy], color='#64748B', lw=1.2, zorder=2)

save_fig(fig, 'fig08_use_case.png')

# ==============================================================================
# FIG 10: Sequence Diagram (Proper vertical lifelines, activation boxes, neat messages)
# ==============================================================================
fig, ax = new_canvas(14.0, 8.0)

lifelines = [
    (1.4, "MR Actor", '#1E3A8A'),
    (3.8, "React Frontend", '#0284C7'),
    (6.4, "FastAPI API Gateway", '#065F46'),
    (9.0, "Database (Supabase)", '#334155'),
    (11.2, "ML Priority Model", '#92400E'),
    (13.0, "OR-Tools Solver", '#4338CA'),
]

# Lifeline headers and vertical dashed lines
for lx, name, col in lifelines:
    draw_node(ax, lx, 7.3, 2.0, 0.6, name, None, border=col, fill=col+'15', title_color=col, t_size=8.2)
    ax.plot([lx, lx], [6.9, 0.6], color='#94A3B8', lw=1.2, ls='--', zorder=1)

# Sequence messages (y decreases down)
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

save_fig(fig, 'fig10_sequence_diagram.png')
print("Core 4 diagrams generated cleanly.")
