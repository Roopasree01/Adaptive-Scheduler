# 🚀 Adaptive CPU Scheduler

**Live Demo:** [Click here to try the app](https://adaptive-scheduler-flame.vercel.app/)

This project started as an assignment, but while working on it, I got genuinely interested in how scheduling works in real systems.

It is an interactive simulation of an **Adaptive Round Robin CPU Scheduler** that dynamically adjusts the **time quantum based on CPU utilization**.

---

## ✨ Features

- Adaptive Time Quantum (2 / 3 / 5 based on CPU load)
- Gantt Chart visualization of process execution
- Waiting Time & Turnaround Time calculation
- Add and delete processes dynamically
- Input validation with UI-based warnings
- Tracks CPU utilization
- Responsive and animated user interface

---

## 🧠 How it works

Unlike traditional Round Robin scheduling with a fixed time quantum, this system adapts dynamically:

- Low CPU usage → increases time quantum  
- High CPU usage → decreases time quantum  
- Moderate usage → keeps it balanced  

This helps improve overall efficiency and reflects more realistic scheduling behavior.

---

## 🏗️ Project Structure

```
.
├── app.py                 # Flask backend (API + routing)
├── core/
│   ├── scheduler.py       # Round Robin scheduling logic
│   ├── memory.py          # Memory management
│   ├── metrics.py         # CPU utilization tracking
│   └── process.py         # Process model
├── frontend/
│   └── index.html
├── requirements.txt  
├── system.py              # Adaptive scheduling system
├── templates/
│   └── index.html         # Frontend UI
├── vercel.json
```

---

## ▶️ How to run

```
git clone https://github.com/your-username/adaptive-scheduler.git
cd adaptive-scheduler
pip install flask
python app.py
```
Open in browser:
```
http://localhost:5000
```

## 🧪 Example Input

```
P1: BT=20 MEM=100 AT=0
P2: BT=20 MEM=100 AT=1
P3: BT=20 MEM=100 AT=2
```
Observe how the time quantum changes dynamically during execution.

## 📊 Output Includes

- Execution timeline (Gantt Chart)
- Dynamic Time Quantum
- CPU Utilization (%)
- Waiting Time
- Turnaround Time

## 💡 TechStack

- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Version Control: GitHub

## 👥 Team

Developed as part of a team project.

## ✨ Worth a star?

If you found this interesting, consider giving it a star!
