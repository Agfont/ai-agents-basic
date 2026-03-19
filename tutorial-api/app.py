from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

LAB_DIR_PATTERN = re.compile(r"^\d+-")
TASK_FILE_PATTERN = re.compile(r"^task_(\d+)_.*\.py$")


@dataclass
class Task:
    id: int
    slug: str
    filename: str
    title: str
    marker_complete: bool


@dataclass
class Lab:
    slug: str
    title: str
    directory: str
    readme: str
    tasks: list[Task]


BASE_DIR = Path(__file__).resolve().parents[1]

app = Flask(__name__)
CORS(app)


def _safe_read_text(path: Path, limit: int = 5000) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:limit]


def _task_title_from_filename(filename: str) -> str:
    name = filename.replace(".py", "")
    name = re.sub(r"^task_\d+_", "", name)
    return name.replace("_", " ").strip().title()


def _task_marker_complete(markers_dir: Path, task_id: int) -> bool:
    if not markers_dir.exists():
        return False

    # Match marker styles like task1_complete.txt, task_1_complete.txt,
    # task1_log.txt (ignored), task5_costs_complete.txt, etc.
    pattern = re.compile(rf"task_?{task_id}.*complete.*\.txt$", re.IGNORECASE)
    for marker in markers_dir.iterdir():
        if marker.is_file() and pattern.search(marker.name):
            return True
    return False


def _discover_labs() -> list[Lab]:
    labs: list[Lab] = []

    for entry in sorted(BASE_DIR.iterdir(), key=lambda p: p.name):
        if not entry.is_dir() or not LAB_DIR_PATTERN.match(entry.name):
            continue

        readme_path = entry / "README.md"
        readme_text = _safe_read_text(readme_path)
        title_line = readme_text.splitlines()[0].strip() if readme_text else entry.name
        title = title_line.lstrip("# ").strip() or entry.name

        markers_dir = entry / "markers"
        tasks: list[Task] = []

        for child in sorted(entry.iterdir(), key=lambda p: p.name):
            if not child.is_file():
                continue
            match = TASK_FILE_PATTERN.match(child.name)
            if not match:
                continue

            task_id = int(match.group(1))
            tasks.append(
                Task(
                    id=task_id,
                    slug=f"task-{task_id}",
                    filename=child.name,
                    title=_task_title_from_filename(child.name),
                    marker_complete=_task_marker_complete(markers_dir, task_id),
                )
            )

        labs.append(
            Lab(
                slug=entry.name,
                title=title,
                directory=entry.name,
                readme=readme_text,
                tasks=tasks,
            )
        )

    return labs


def _lab_by_slug(lab_slug: str) -> Lab | None:
    for lab in _discover_labs():
        if lab.slug == lab_slug:
            return lab
    return None


def _task_by_id(lab: Lab, task_id: int) -> Task | None:
    for task in lab.tasks:
        if task.id == task_id:
            return task
    return None


def _run_python_file(lab_dir: Path, filename: str) -> dict[str, Any]:
    command = [sys.executable, filename]
    timeout_sec = int(request.args.get("timeout", 120))

    try:
        completed = subprocess.run(
            command,
            cwd=str(lab_dir),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
            env={**os.environ},
        )
        return {
            "ok": completed.returncode == 0,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "command": " ".join(command),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "exit_code": -1,
            "stdout": exc.stdout or "",
            "stderr": f"Timed out after {timeout_sec}s",
            "command": " ".join(command),
        }


@app.get("/api/health")
def health() -> Any:
    return jsonify({"status": "ok"})


@app.get("/api/labs")
def list_labs() -> Any:
    labs = _discover_labs()
    payload = []
    for lab in labs:
        payload.append(
            {
                "slug": lab.slug,
                "title": lab.title,
                "directory": lab.directory,
                "task_count": len(lab.tasks),
            }
        )
    return jsonify(payload)


@app.get("/api/labs/<lab_slug>")
def get_lab(lab_slug: str) -> Any:
    lab = _lab_by_slug(lab_slug)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404
    return jsonify(asdict(lab))


@app.get("/api/labs/<lab_slug>/tasks/<int:task_id>")
def get_task(lab_slug: str, task_id: int) -> Any:
    lab = _lab_by_slug(lab_slug)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404

    task = _task_by_id(lab, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task_path = BASE_DIR / lab.directory / task.filename
    return jsonify(
        {
            "lab": {"slug": lab.slug, "title": lab.title, "directory": lab.directory},
            "task": asdict(task),
            "source": _safe_read_text(task_path, limit=12000),
        }
    )


@app.get("/api/labs/<lab_slug>/tasks/<int:task_id>/status")
def get_task_status(lab_slug: str, task_id: int) -> Any:
    lab = _lab_by_slug(lab_slug)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404

    task = _task_by_id(lab, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    markers_dir = BASE_DIR / lab.directory / "markers"
    return jsonify(
        {
            "lab": lab.slug,
            "task_id": task.id,
            "marker_complete": _task_marker_complete(markers_dir, task.id),
        }
    )


@app.post("/api/labs/<lab_slug>/tasks/<int:task_id>/run")
def run_task(lab_slug: str, task_id: int) -> Any:
    lab = _lab_by_slug(lab_slug)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404

    task = _task_by_id(lab, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    lab_dir = BASE_DIR / lab.directory
    result = _run_python_file(lab_dir, task.filename)

    markers_dir = lab_dir / "markers"
    result["marker_complete"] = _task_marker_complete(markers_dir, task.id)
    return jsonify(result)


@app.post("/api/labs/<lab_slug>/verify-environment")
def run_verify_environment(lab_slug: str) -> Any:
    lab = _lab_by_slug(lab_slug)
    if not lab:
        return jsonify({"error": "Lab not found"}), 404

    verify_path = BASE_DIR / lab.directory / "verify_environment.py"
    if not verify_path.exists():
        return jsonify({"error": "verify_environment.py not found"}), 404

    result = _run_python_file(BASE_DIR / lab.directory, "verify_environment.py")
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_RUN_PORT", "5050"))
    app.run(host="0.0.0.0", port=port, debug=True)
