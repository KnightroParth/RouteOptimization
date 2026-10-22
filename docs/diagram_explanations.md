# System Architecture & Diagram Explanation Guide
**Project:** Medical Representative (MR) Visit Prioritization & Route Optimization System  
**Prepared for:** Project Review III, Technical Documentation & System Defense  
**Location of Visuals:** [`docs/diagrams/`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams)

---

## Table of Contents
1. [Overview & Diagram Catalog](#overview--diagram-catalog)
2. [Figure 1: Problem Context & Domain Challenges (`fig01_problem_context.png`)](#figure-1-problem-context--domain-challenges)
3. [Figure 2: Research Gap & End-to-End Integrated Framework (`fig02_research_gap.png`)](#figure-2-research-gap--end-to-end-integrated-framework)
4. [Figure 3: Project Gantt Timeline (`fig03_gantt_timeline.png`)](#figure-3-project-gantt-timeline)
5. [Figure 4: Task Network & Dependency Architecture (`fig04_task_network.png`)](#figure-4-task-network--dependency-architecture)
6. [Figure 5: Software Development Life Cycle (SDLC) Model (`fig05_sdlc_model.png`)](#figure-5-software-development-life-cycle-sdlc-model)
7. [Figure 6: 4-Tier Enterprise System Architecture (`fig06_architecture.png`)](#figure-6-4-tier-enterprise-system-architecture)
8. [Figure 7: End-to-End Data Flow Pipeline (`fig07_data_flow.png`)](#figure-7-end-to-end-data-flow-pipeline)
9. [Figure 8: UML Use Case Diagram (`fig08_use_case.png`)](#figure-8-uml-use-case-diagram)
10. [Figure 9: MR Field Activity Diagram (`fig09_activity_mr.png`)](#figure-9-mr-field-activity-diagram)
11. [Figure 10: UML Sequence Diagram (`fig10_sequence_diagram.png`)](#figure-10-uml-sequence-diagram)
12. [Figure 11: UML Class Diagram (`fig11_class_diagram.png`)](#figure-11-uml-class-diagram)
13. [Figure 12: Entity-Relationship (ER) Schema (`fig12_er_diagram.png`)](#figure-12-entity-relationship-er-schema)
14. [Figure 13: Route & Visit State Machine Diagram (`fig13_state_diagram.png`)](#figure-13-route--visit-state-machine-diagram)
15. [Figure 14: Component Diagram (`fig14_component_diagram.png`)](#figure-14-component-diagram)
16. [Figure 15: Physical Deployment Diagram (`fig15_deployment_diagram.png`)](#figure-15-physical-deployment-diagram)
17. [Figure 16: Machine Learning Feature & Scoring Pipeline (`fig16_ml_pipeline.png`)](#figure-16-machine-learning-feature--scoring-pipeline)

---

## Overview & Diagram Catalog

This document provides complete technical, functional, and architectural documentation for the 16 system diagrams generated for the **Medical Representative Visit Prioritization and Route Optimization System**. 

The diagrams provide end-to-end coverage across all software engineering dimensions:
- **Conceptual & Domain Modeling:** Figures 1, 2, 8
- **Project Engineering & Methodology:** Figures 3, 4, 5
- **System Architecture & Data Flows:** Figures 6, 7, 14, 15
- **Behavioral & Interaction Modeling:** Figures 9, 10, 13
- **Structural & Data Models:** Figures 11, 12
- **Analytics & Scoring Pipeline:** Figure 16

---

## Figure 1: Problem Context & Domain Challenges
**File:** [`docs/diagrams/fig01_problem_context.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig01_problem_context.png)

### 1. Conceptual Description
Medical representatives in commercial pharmaceutical distribution operate under highly constrained, multi-variable daily environments. Figure 1 structures the fundamental domain bottleneck into four input factors converging onto the traditional manual planning approach, causing severe operational inefficiencies:
1. **Multiple Doctors:** Each MR is assigned 100–150 doctors across diverse medical specialties (Cardiology, Orthopedics, Pediatrics, General Medicine, Oncology).
2. **Varying Priorities:** Doctors have vastly different prescription volumes, time since last visit, and strategic value. Some require weekly detailing; others only monthly.
3. **Strict Time Windows:** Clinics maintain tight consultation hours (e.g., 09:30–11:30 AM or 05:00–07:00 PM). Visiting outside these narrow slots results in refusal of entry.
4. **Dispersed Locations:** Doctor clinics are geographically scattered across congested urban traffic zones, creating unpredictable travel overheads.

### 2. Failure Mode of Manual Planning
When field representatives rely on intuition, manual notebooks, or static spreadsheets, they cannot mentally co-optimize combinatorial constraints:
$$\text{Doctor Priority} \times \text{Clinic Time Windows} \times \text{Transit Distance} \times \text{Max Working Shift}$$
The resulting outcome is sub-optimal: excessive criss-cross transit, long waiting in clinic lobbies, missed Tier-1 doctor visits, and high representative fatigue and burnout.

### 3. Viva / Presentation Talking Points
- *"Manual planning suffers from combinatorial explosion: with just 10 doctors, there are over 3.6 million possible permutations of visitation sequences."*
- *"Without algorithmically bounded time windows, MRs frequently arrive during closed hours, wasting productive field time."*

---

## Figure 2: Research Gap & End-to-End Integrated Framework
**File:** [`docs/diagrams/fig02_research_gap.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig02_research_gap.png)

### 1. Conceptual Description
Figure 2 illustrates the core intellectual and engineering contribution of this project: bridging the gap between data-driven visit prioritization and spatial routing optimization into a continuous automated closed loop.

Traditional literature and enterprise CRM software treat prioritization and vehicle routing as separate silos:
- CRM systems rank doctors statically without spatial awareness.
- GPS routing engines optimize shortest paths without clinical priority or time windows.

### 2. Integrated Workflow Steps
1. **Historical & Visit Data:** Supabase database stores past visit histories, detailing notes, days elapsed, and prescriber tiers.
2. **ML Priority Engine:** Evaluates multidimensional features using a trained Random Forest model to assign calibrated urgency scores ($0.00$ to $1.00$).
3. **Operational Constraints:** Doctor availability time windows, MR working hours, and inter-clinic distance/duration matrices.
4. **Google OR-Tools Solver:** A Vehicle Routing Problem with Time Windows (VRPTW) mathematical engine calculates the optimal visitation sequence that maximizes high-priority coverage while minimizing total distance and wait time.
5. **Feasible Daily Schedule:** Produces a sequenced, turn-by-turn itinerary with exact arrival times and departure deadlines.
6. **Role-Based Dashboards:** Displays interactive Leaflet maps and actionable checklists for MRs, and territory compliance analytics for Area Sales Managers.

---

## Figure 3: Project Gantt Timeline
**File:** [`docs/diagrams/fig03_gantt_timeline.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig03_gantt_timeline.png)

### 1. Conceptual Description
Figure 3 defines the 16-week academic project execution timeline across 8 structured milestones:
- **Weeks 1–3:** Problem Definition, Stakeholder Analysis & Comprehensive Literature Survey.
- **Weeks 2–4:** Software Requirements Specification (SRS) & Scope Freezing.
- **Weeks 3–6:** PostgreSQL/Supabase Relational Database Schema Design & Seed Data Generation.
- **Weeks 5–8:** Machine Learning Priority Model Formulation, Feature Engineering & Hyperparameter Tuning.
- **Weeks 7–11:** Google OR-Tools VRPTW Mathematical Formulation, Solver Integration & Heuristic Calibration.
- **Weeks 8–13:** Frontend React Dashboard (Vite, Leaflet, Tailwind/Vanilla CSS) & FastAPI REST Endpoints.
- **Weeks 11–15:** End-to-End Pipeline Integration, Stress Testing & Urban Field Validation.
- **Weeks 13–16:** Technical Documentation, LaTeX Final Report, Review III & Viva Defense.

---

## Figure 4: Task Network & Dependency Architecture
**File:** [`docs/diagrams/fig04_task_network.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig04_task_network.png)

### 1. Conceptual Description
Figure 4 models the project's critical path and architectural dependencies through tasks T1 through T7:
- **T1 (Requirements & Scope):** Unlocks schema design and domain constraints.
- **T2 (Data Schema & Validation):** Serves as the dual foundation for both model training (T3) and UI wireframing (T5).
- **T3 (ML Priority Model) & T4 (Route Optimizer):** Form the intelligence pipeline, feeding solved mathematical itineraries directly into Web Dashboards (T5).
- **T6 (System Integration & E2E Tests):** Validates API payloads, JWT tokens, and solver convergence before final Review III evaluation (T7).

---

## Figure 5: Software Development Life Cycle (SDLC) Model
**File:** [`docs/diagrams/fig05_sdlc_model.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig05_sdlc_model.png)

### 1. Conceptual Description
Figure 5 illustrates the **Iterative Evolutionary Prototyping** model adopted for this system:
1. **Requirements:** Defining domain constraints (time windows, battery/fuel limits, doctor availability).
2. **System Design:** UML class/sequence diagrams, database normal forms, and REST contract schemas.
3. **Implementation:** Python FastAPI backend, scikit-learn models, OR-Tools solver, and React SPA.
4. **Verification:** Unit testing, solver feasibility boundary tests, and cross-validation of ML predictions.
5. **Review & Demo:** Stakeholder review and feedback loop driving continuous algorithmic refinement.

---

## Figure 6: 4-Tier Enterprise System Architecture
**File:** [`docs/diagrams/fig06_architecture.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig06_architecture.png)

### 1. Conceptual Description
Figure 6 presents the enterprise-grade layered architecture of the deployed application:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. PRESENTATION LAYER (React SPA / Leaflet Maps / Responsive UI)       │
│    - MR Daily Execution Portal (Beat Checklist, Navigation, Logging)   │
│    - Manager Performance Dashboard (Territory KPIs, Compliance)        │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ HTTPS / REST / JSON
┌────────────────────────────────────▼───────────────────────────────────┐
│ 2. APPLICATION & API GATEWAY LAYER (FastAPI Framework)                 │
│    - REST Endpoints (/routes, /visits, /doctors, /auth)                │
│    - JWT Security & Role-Based Access Control (RBAC)                   │
│    - Service Orchestrator (Coordinates ML & Optimization Pipelines)    │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ Async Subsystem Dispatch
┌────────────────────────────────────▼───────────────────────────────────┐
│ 3. INTELLIGENCE CORE (Optimization & Machine Learning)                 │
│    - Priority Scoring Engine (Random Forest / Feature Transformer)     │
│    - Route Optimizer (Google OR-Tools VRPTW Solver Engine)             │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ SQL Alchemy / AsyncPG
┌────────────────────────────────────▼───────────────────────────────────┐
│ 4. PERSISTENCE & DATA ACCESS LAYER (Supabase Cloud PostgreSQL 15+)     │
│    - Relational Storage (Users, Doctors, Appointments, Route Stops)    │
│    - Precomputed Distance-Time Matrices & Historical Audit Logs        │
└────────────────────────────────────────────────────────────────────────┘
```

### 2. Architectural Separation of Concerns
- The **Presentation Layer** remains stateless, rendering high-performance interactive maps and tables.
- The **Gateway Layer** validates incoming payloads and handles authentication before offloading compute.
- The **Intelligence Core** runs isolated from web server threads to prevent blocking during intensive mathematical matrix solving.
- The **Persistence Layer** maintains strict relational integrity with foreign keys and geolocation indices.

---

## Figure 7: End-to-End Data Flow Pipeline
**File:** [`docs/diagrams/fig07_data_flow.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig07_data_flow.png)

### 1. Sequential Pipeline Stages
Figure 7 traces the journey of a single user request from button press to map rendering:
1. **MR Login:** JWT authentication validates field representative identity and territory scope.
2. **Select Date & Territory:** Representative selects target date (e.g., today's beat).
3. **Query Doctors & Appointments:** Backend retrieves candidate doctors and scheduled consultation windows.
4. **Feature Engineering:** Computes dynamic features ($recency$, $Rx\_volume$, $conversion\_rate$, $time\_window$).
5. **Priority Scoring:** Evaluates vector inputs to produce urgency classifications ($High$, $Medium$, $Low$).
6. **VRPTW Optimizer:** Passes prioritized doctors and travel times into Google OR-Tools.
7. **Generate Route Plan:** Computes an ordered sequence of stops with optimal ETAs and minimal total transit.
8. **Map Dashboard:** Returns JSON payload to React frontend, which renders markers, polyline routes, and stop timelines.

---

## Figure 8: UML Use Case Diagram
**File:** [`docs/diagrams/fig08_use_case.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig08_use_case.png)

### 1. Primary Actors & System Boundaries
- **Medical Representative (MR):**
  - Authenticate & Sign In
  - View Today's Assigned Visits
  - Request Route Optimization
  - View Route on Map & Timeline
  - Log Visit Status (Pending $\rightarrow$ In-Progress $\rightarrow$ Completed / Rescheduled)
  - Transmit WhatsApp En-Route ETA Notifications
- **Field Sales Manager:**
  - Authenticate & Sign In
  - Manage Doctor Master Database & Territory Assignments
  - Monitor Team Field Execution in Real Time
  - Review Territory Analytics, Fuel Savings, and Compliance KPIs
  - Export Audit Logs for Compliance Review

---

## Figure 9: MR Field Activity Diagram
**File:** [`docs/diagrams/fig09_activity_mr.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig09_activity_mr.png)

### 1. Workflow Logic & Decision Gates
Figure 9 tracks the field representative's physical execution loop:
1. **Start:** Field rep authenticates via the mobile web portal at 08:30 AM.
2. **Fetch Schedule:** Inspects today's prioritized candidate list.
3. **Generate Optimized Route:** Triggers the solver, which locks the sequence based on morning clinic slots.
4. **Travel to Stop Location:** Follows turn-by-turn map coordinates to Doctor $k$.
5. **Decision Diamond (Doctor Available?):**
   - **Yes:** Representative conducts detailing session, hands over drug samples, and logs outcomes in the system.
   - **No (Emergency surgery / clinic closed):** Representative marks stop as *Missed/Delayed* with justification note.
6. **Decision Diamond (More Stops in Daily Shift?):**
   - **Yes:** Moves immediately to next scheduled waypoint in sequence.
   - **No:** Finishes daily beat route $\rightarrow$ triggers shift summary $\rightarrow$ End Day.

---

## Figure 10: UML Sequence Diagram
**File:** [`docs/diagrams/fig10_sequence_diagram.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig10_sequence_diagram.png)

### 1. Inter-Component Communication Lifelines
Figure 10 formally models synchronous and asynchronous message exchanges:
- `MR Actor` clicks **Generate Route** in `React Frontend`.
- `React Frontend` sends `POST /api/routes/generate` with JWT bearer token to `FastAPI Gateway`.
- `FastAPI Gateway` queries `Supabase DB` for assigned doctor coordinates and appointment availability windows.
- `Supabase DB` returns records to `FastAPI Gateway`.
- `FastAPI Gateway` dispatches feature vectors to `ML Engine` via `predict_priority(features)`.
- `ML Engine` returns priority classifications ($High$, $Medium$, $Low$) with confidence scores.
- `FastAPI Gateway` calls `solve_vrptw(matrix, windows, priorities)` on `OR-Tools Engine`.
- `OR-Tools Engine` solves the mathematical model and returns the optimal sequence with arrival timestamps.
- `FastAPI Gateway` executes `INSERT INTO routes, route_stops` in `Supabase DB` to persist the itinerary.
- `FastAPI Gateway` returns `HTTP 200 OK` with full GeoJSON polyline and stop schedule to `React Frontend`.

---

## Figure 11: UML Class Diagram
**File:** [`docs/diagrams/fig11_class_diagram.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig11_class_diagram.png)

### 1. Domain Entities & Object Relationships
- **User:** `user_id`, `email`, `role` (MR / Manager), `created_at`; methods: `authenticate()`, `get_profile()`.
- **MedicalRep:** `mr_id`, `user_id` (FK), `territory`, `max_daily_hours`; methods: `request_daily_route()`, `update_status()`. Cardinality with User is $1 : 0..1$.
- **Doctor:** `doctor_id`, `specialty`, `lat`, `lon`, `window_start`, `window_end`; methods: `get_schedule()`, `is_available()`.
- **PriorityPrediction:** `pred_id`, `doctor_id` (FK), `priority_score`, `priority_class`; methods: `predict()`, `explain_factors()`. Cardinality with Doctor is $1 : N$.
- **Route:** `route_id`, `mr_id` (FK), `plan_date`, `total_dist_km`, `total_time_min`; methods: `optimize_vrptw()`, `export_geojson()`. Cardinality with MedicalRep is $1 : N$.
- **RouteStop:** `stop_id`, `route_id` (FK), `doctor_id` (FK), `sequence`, `eta`, `etd`; methods: `mark_visited()`, `log_outcome()`. Composition with Route ($1 : 1..N$) and association with PriorityPrediction ($1 : 1$).

---

## Figure 12: Entity-Relationship (ER) Schema
**File:** [`docs/diagrams/fig12_er_diagram.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig12_er_diagram.png)

### 1. Relational Database Tables
- **`USERS`:** Primary key `user_id` (INT), `email` (VARCHAR), `password_hash` (VARCHAR), `role` (ENUM: `'mr'`, `'mgr'`), `created_at` (TIMESTAMP).
- **`MEDICAL_REPS`:** Primary key `mr_id` (INT), Foreign key `user_id` $\rightarrow$ `USERS.user_id` ($1 : 1$), `territory_name`, `start_lat`, `start_lon`, `work_hours_limit`.
- **`DOCTORS`:** Primary key `doctor_id` (INT), `name`, `specialization`, `lat`, `lon` (DECIMAL), `avail_start`, `avail_end` (TIME), `visit_duration` (INT).
- **`PREDICTIONS`:** Primary key `pred_id` (INT), Foreign key `doctor_id` $\rightarrow$ `DOCTORS.doctor_id` ($1 : N$), `priority_score` (FLOAT), `priority_level` (VARCHAR), `model_version`.
- **`ROUTES`:** Primary key `route_id` (INT), Foreign key `mr_id` $\rightarrow$ `MEDICAL_REPS.mr_id` ($1 : N$), `plan_date` (DATE), `total_distance_km` (FLOAT), `total_duration_min` (FLOAT), `status` (ENUM).
- **`ROUTE_STOPS`:** Primary key `stop_id` (INT), Foreign key `route_id` $\rightarrow$ `ROUTES.route_id` ($1 : N$), Foreign key `doctor_id` $\rightarrow$ `DOCTORS.doctor_id`, `sequence_order` (INT), `est_arrival`, `departure` (TIME), `status` (ENUM).

---

## Figure 13: Route & Visit State Machine Diagram
**File:** [`docs/diagrams/fig13_state_diagram.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig13_state_diagram.png)

### 1. Lifecycle Transitions
Figure 13 governs state integrity throughout the planning and execution lifecycle:
- **`Draft Request`:** Initial parameter selection. If time windows conflict, transitions to `Validation Failed` $\rightarrow$ rep prompts parameter correction.
- **`Validated Plan`:** Input validated against operational boundaries $\rightarrow$ triggers solver.
- **`Optimizing Route`:** Active OR-Tools execution state.
- **`Scheduled`:** Optimal route generated, stored, and displayed on map.
- **`In Progress`:** Representative initiates field route; stops update dynamically.
- **`Completed`:** All scheduled appointments visited or resolved $\rightarrow$ shift summary locked.

---

## Figure 14: Component Diagram
**File:** [`docs/diagrams/fig14_component_diagram.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig14_component_diagram.png)

### 1. Micro-Component Decoupling
Figure 14 outlines clean separation between services:
- **React Web Application:** Handles UI presentation, state, and Leaflet map rendering.
- **FastAPI REST Server:** Acts as controller gateway, verifying tokens and marshaling payloads.
- **ML Priority Engine:** Microservice exposing feature extraction and classification interfaces.
- **Route Optimizer:** Standalone OR-Tools solver component invoked via clean API abstraction.
- **Persistence Module:** Supabase ORM layer managing transactional consistency.

---

## Figure 15: Physical Deployment Diagram
**File:** [`docs/diagrams/fig15_deployment_diagram.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig15_deployment_diagram.png)

### 1. Production Topology
Figure 15 details the modern cloud deployment infrastructure:
- **Client Browser Node (Desktop / Mobile):** React SPA hosted on Vercel Edge with global CDN caching and HTTPS / TLS 1.3 encryption.
- **FastAPI Application Server Node:** Python 3.12 running inside a containerized Uvicorn ASGI instance on a cloud VM.
- **Database Server Node:** Managed PostgreSQL 15+ cluster hosted on Supabase Cloud via SSL Port 5432.
- **Routing Matrix API Node:** High-speed distance-duration matrix engine (OSRM / Maps Directions API) over HTTPS REST.

---

## Figure 16: Machine Learning Feature & Scoring Pipeline
**File:** [`docs/diagrams/fig16_ml_pipeline.png`](file:///d:/Projects/MR%20Route%20Optimization/docs/diagrams/fig16_ml_pipeline.png)

### 1. Data Transformation & Model Workflow
Figure 16 breaks down the step-by-step scoring engine:
1. **Raw Visit Data:** Historical interaction logs, doctor visit dates, and detailing notes.
2. **Preprocessing:** Handling missing values, standardizing dates, and one-hot encoding clinic specialties.
3. **Feature Pipeline:** Generates 5 engineered metrics:
   - *Recency:* Days since previous detailing session (35% weight).
   - *Rx Potential:* Prescription volume tier (25% weight).
   - *Conversion Rate:* Historical responsiveness ratio (15% weight).
   - *Time Window Fit:* Feasibility of clinic consultation hours (15% weight).
   - *Specialty Alignment:* Strategic fit with active drug campaigns (10% weight).
4. **Model Training:** Random Forest classifier with 100 decision trees and 10-fold cross validation.
5. **Priority Classes:** Emits calibrated probabilities mapped into three distinct operational tiers:
   - **High Priority:** Probability $> 0.70$ (Mandatory inclusion in daily itinerary with high penalty factor if omitted).
   - **Medium Priority:** Probability $0.40 - 0.70$ (Secondary stops scheduled if time window and transit budget permit).
   - **Low Priority:** Probability $< 0.40$ (Deferred to subsequent weekly beat cycles).

---

## Summary for Viva & Defense Presentations

When presenting these diagrams during project reviews or technical evaluations, emphasize the following key themes:
1. **Mathematical Rigor:** The system does not merely "plot points on a map"—it solves an NP-hard Vehicle Routing Problem with Time Windows (VRPTW) utilizing exact mathematical constraints.
2. **Clinical Practicality:** By incorporating doctor availability windows, visit durations, and priority weights, the generated schedule directly mirrors real-world pharmaceutical sales dynamics.
3. **Enterprise Architecture:** Clean separation across presentation, application gateway, intelligence core, and database tiers ensures high reliability, sub-second latency, and horizontal scalability.
