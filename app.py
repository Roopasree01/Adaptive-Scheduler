from flask import Flask, render_template, request, jsonify
from core.process import Process
from core.system import AdaptiveSystem

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['POST'])
def run_simulation():
    data = request.json

    total_mem = int(data.get('memory', 500))
    raw = data.get('processes') or []

    for i, p in enumerate(raw):
        need = int(p.get('mem', 0))
        if need > total_mem:
            return jsonify({
                "gantt": [],
                "results": [],
                "halt_reason": (
                    f"P{i + 1} needs {need} memory but the system only has {total_mem}. "
                    "Lower that process's memory or increase total system memory."
                ),
            }), 200

    processes = []
    for i, p in enumerate(raw):
        processes.append(Process(f"P{i+1}", p['bt'], p['mem'], p['at']))

    system = AdaptiveSystem(processes, total_mem, data['tq'])
    system.run()

    return jsonify({
        "gantt": system.gantt,
        "results": [
            {
                "pid": p.pid,
                "wt": p.waiting_time,
                "tat": p.turnaround_time
            } for p in processes
        ],
        "halt_reason": system.halt_reason,
        "cpu_util": system.metrics.cpu_utilization(system.time)
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)