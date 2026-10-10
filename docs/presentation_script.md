# Project Review III Presentation Script
**AI-Based Medical Representative Visit Prioritization and Route Optimization**

## Slide 1: Title Slide (Speaker 1)
"Good morning everyone. We are Group 19, and today we will be presenting our Project Review III for the topic 'AI-Based Medical Representative Visit Prioritization and Route Optimization'. I am [Your Name], and I'm joined by my teammates [Teammate 1] and [Teammate 2]. Our project is guided by Prof. M. U. Buchade."

## Slide 2: Problem Statement (Speaker 1)
"To start with, let's look at the core problem. Medical Representatives, or MRs, have a demanding job of visiting multiple doctors every single day. Planning these visits manually becomes incredibly difficult. Why? Because each doctor has their own priority, specific availability windows, different locations, and varying visit durations.
When you combine multiple doctors, different priorities, tight time windows, and the MR's limited working hours, manual planning often leads to inefficient routes and missed high-priority visits. Our system aims to solve this."

## Slide 3: Abstract (Speaker 1)
"In our proposed system, we introduce an AI-based web application to automate and optimize this process. We use a Machine Learning model to predict the priority of a visit based on historical data. Then, we feed this priority—along with appointment times, working hours, and travel data—into Google OR-Tools. The result is a mathematically optimized daily route that respects all constraints, ensuring MRs visit the most important doctors at the right time."

## Slide 4: Why this project? (Speaker 1)
"So, why is this project necessary? The current manual process creates three major bottlenecks:
1. **The Prioritization Problem:** Which doctor should be visited first?
2. **The Scheduling Problem:** When exactly can the doctor be visited?
3. **The Routing Problem:** In what sequence should these doctors be visited to minimize travel?
We address 'Who to prioritize' using Machine Learning, and 'Where and when to go' using Optimization algorithms."

## Slide 5: Existing System (Speaker 1)
"In the current existing system, a manager or MR manually selects doctors, checks their availability, and tries to arrange visits by estimating travel times. It's a tedious, trial-and-error approach that often results in suboptimal schedules and wasted travel time."

## Slide 6 & 7: Research Gap (Speaker 2)
"Moving on to our literature survey and the research gap. Existing research often treats visit prioritization, appointment scheduling, and vehicle routing as completely separate problems. 
Our major contribution is the **integration** of data-driven prioritization (using ML) with constraint-based route optimization (using OR-Tools) into a single, unified decision-support workflow for MRs."

## Slide 8 & 9: Proposed Solution & Methodology (Speaker 2)
"Our proposed solution consists of three intelligence layers:
1. **Prediction (ML):** Determining visit priority.
2. **Optimization (OR-Tools):** Generating the sequence and schedule using VRPTW (Vehicle Routing Problem with Time Windows).
3. **Application:** A web dashboard for both MRs and Managers.

Our methodology spans six phases: Data Collection and Preprocessing, training the ML model for priority, building the Optimization matrix, developing the Web Application (using FastAPI, React, and MySQL), and finally, System Evaluation."

## Slide 10, 11 & 12: Design and Architecture (Speaker 2)
"This is our System Architecture and Data Flow. 
When an MR logs in and selects a date, the system retrieves assigned doctors and appointment constraints. The ML model evaluates these and generates priority scores. These scores, combined with a travel matrix, are passed to OR-Tools, which outputs an optimized route sequence displayed on the MR's dashboard."

## Slide 13 & 14: Machine Learning (Speaker 3)
"Let's dive into the Machine Learning layer. The ML model predicts the priority of a visit based on features like 'days since last visit', 'visit frequency', 'appointment status', and 'follow-up requirements'. 
For example, if Doctor A hasn't been visited in 25 days, requires a follow-up, and has a confirmed appointment, our Random Forest classifier will assign a High priority. Conversely, a recently visited doctor with flexible availability might get a lower priority score."

## Slide 15 & 16: Optimization (Speaker 3)
"For Optimization, we treat this as a Vehicle Routing Problem with Time Windows. 
Our objective is to minimize total travel time and waiting time, while applying a penalty for missing high-priority visits. The route is subject to strict constraints: doctor availability, MR working hours, visit duration, and route feasibility."

## Slide 17 & 18: Implementation & Modules (Speaker 3)
"Our implementation is broken down into several modules: Authentication, Doctor and MR Management, Visit Management, the ML Priority Engine, the Route Optimization core, and the separate dashboards for MRs and Managers. This modular approach ensures a robust and scalable application."

## Slide 19, 20, 21 & 22: Working Flow & UI (Speaker 1)
"Here we demonstrate the working flow. The MR's dashboard shows today's visits. By clicking 'Generate Optimized Route', the system triggers OR-Tools and returns a sequenced list of visits with specific appointment times. 
The Manager's dashboard provides a bird's-eye view—showing total planned visits, completed vs. pending tasks, and completion rates of high-priority visits. This ensures full transparency."

## Slide 23 & 24: Tech Stack & Database (Speaker 1)
"Our technology stack leverages modern frameworks: React for the frontend, FastAPI (Python) for the backend, MySQL for the database, and Google OR-Tools with scikit-learn for the core AI logic. Our database is relationally designed to link Users, Doctors, Appointments, and Optimized Routes efficiently."

## Slide 25 & 26: Evaluation (Speaker 1)
"For evaluation, we establish a baseline comparison. We take a manual, baseline plan and compare it against the plan generated by our proposed system using the same input. We will measure metrics like total distance traveled, time saved, and the percentage of high-priority visits successfully completed."

## Slide 27, 28 & 29: Risks & Limitations (Speaker 1)
"We have identified potential risks, such as unpredictable traffic or sudden changes in doctor availability, which our system handles by allowing dynamic rescheduling. We also ensure data privacy for doctor and agency records. A current limitation is that the travel matrix relies on static or pre-computed API data rather than real-time traffic."

## Slide 30, 31 & 32: Outlook & Progress (Speaker 1)
"Looking ahead, future scopes include integrating real-time GPS tracking and live traffic updates. 
In Semester-I, we finalized our problem, completed the literature survey, data requirements, architecture, and initial prototype. Currently in Semester-II, we are focusing on integrating the ML model with the OR-Tools optimizer and polishing the web application for deployment.
Thank you for your time. We are now open for questions."
