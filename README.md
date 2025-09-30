# ðŸ¤° Perinatal Support Scheduler

![Java](https://img.shields.io/badge/Java-Programming-orange?logo=java&logoColor=white&style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Academic%20Research-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

---

## ðŸ“– Project Overview
The **Perinatal Support Scheduler** is an academic project that proposes a **digital scheduling system** to support pregnant women and new mothers.  
It connects mothers with trained volunteers (doulas, nurses, helpers) and ensures **continuity of care**, **risk-based prioritization**, and **efficient scheduling**.

The systemâ€™s aim is to **reduce maternal stress and health risks by ~10%** through timely scheduling and better volunteer-mother coordination.

---

## ðŸŽ¯ Key Objectives
- Provide mothers with **timely access** to prenatal and postnatal support.  
- Ensure **priority scheduling** for high-risk mothers.  
- Enable **volunteers** to set availability and service limits.  
- Allow **admins** to monitor schedules, resolve conflicts, and generate reports.  

---

## ðŸ—ï¸ Core Features
### ðŸ‘© Mothers
- Register with personal details, due date, and risk level.  
- Request, reschedule, or cancel visits.  
- Upload medical documents.  
- Receive confirmations, reminders, and notifications.  
- Provide feedback after visits.  

### ðŸ‘©â€âš•ï¸ Volunteers
- Register with skills and certifications.  
- Submit weekly availability & set service limits.  
- Accept/reject visits and mark them as completed.  
- Receive notifications and view feedback.  

### ðŸ‘¨â€ðŸ’¼ Admins
- Approve/reject profiles.  
- Monitor visit schedules and resolve conflicts.  
- Reassign volunteers when needed.  
- Generate statistics and manage **risk-priority assignments**.  

---

## âš™ï¸ Non-Functional Requirements
- **Performance:** Respond within 3 seconds under normal load.  
- **Scalability:** Support up to 10,000 users.  
- **Availability:** 99.5% uptime.  
- **Security:** Encrypted maternal records & secure password storage.  
- **Accessibility:** Mobile-first, multilingual, WCAG 2.1 AA compliant.  

---

## ðŸ“Š System Diagrams

### Use Case Diagram (Functional Model)
![Use Case â€“ Functional](diagrams/functional_model_diagram_1.png)

### Use Case Diagram (Structural & Behavioral)
![Use Case â€“ Structural/Behavioral](diagrams/structural_behavioral_model_diagram_1.png)

### Activity Diagram
![Activity](diagrams/functional_model_diagram_2.png)

### Class Diagram
![Class](diagrams/structural_behavioral_model_diagram_2.png)

### Object Diagram
![Object](diagrams/structural_behavioral_model_diagram_3.png)

### Sequence Diagram
![Sequence](diagrams/structural_behavioral_model_diagram_4.png)

### Behavioral State Machine
![State Machine](diagrams/structural_behavioral_model_diagram_5.png)

---

## ðŸ—‚ï¸ Diagrams Legend
- **Use Case Diagram (Functional Model)** â†’ Shows the interactions between Mothers, Volunteers, Admins, and the system.  
- **Use Case Diagram (Structural & Behavioral)** â†’ Same scope but mapped to class/structural model for traceability.  
- **Activity Diagram** â†’ Illustrates workflows like scheduling and rescheduling visits.  
- **Class Diagram** â†’ Defines system entities such as Mother, Volunteer, Visit, Notification, and their relationships.  
- **Object Diagram** â†’ Snapshot of objects and their state at a given moment (e.g., a scheduled visit).  
- **Sequence Diagram** â†’ Shows message flows (e.g., scheduling request from Mother â†’ System â†’ Volunteer).  
- **Behavioral State Machine** â†’ Tracks a Visit lifecycle: Requested â†’ Assigned â†’ Confirmed â†’ Completed.  

---

## ðŸ“‚ Repository Contents
- `System_Request/` â†’ Business need, scope, and value  
- `Requirements_Definition/` â†’ Functional & non-functional requirements  
- `Functional_Model/` â†’ Use case descriptions, activity diagrams  
- `Structural_Behavioral_Model/` â†’ Class, object, sequence, and state machine diagrams  
- `diagrams/` â†’ Extracted PNG diagrams  
- `References/` â†’ Research articles and academic sources  

---

## ðŸ“Œ References
- Dennis, A., Wixom, B., & Tegarden, D. (2020). *Systems Analysis and Design: An Object-Oriented Approach with UML (6th ed.)*. Wiley Global Education US.  
- Richter, F. (2024, June 24). *The U.S. lags behind in fight against maternal mortality*. Statista.  

---

## ðŸ‘¨â€ðŸŽ“ Author
**Satish Varada**  
Masterâ€™s Student, **Rivier University**  
ðŸ“§ Email: svarada@rivier.edu  

---

â­ If you found this repository useful, donâ€™t forget to **star it**!
