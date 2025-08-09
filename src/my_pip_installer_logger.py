import logging
import subprocess
import json
from io import StringIO
from typing import List, Dict

def run_pip_install_summary(packages: List[str]) -> Dict[str, Dict]:
    """Install pip packages with clean summary and safe repeated use."""
    
    # In-memory log buffer
    log_buffer = StringIO()

    # Set up pip logger fresh every time
    pip_logger = logging.getLogger("pip_logger")
    pip_logger.setLevel(logging.INFO)
    pip_logger.propagate = False  # ✅ Prevent Jupyter log echoing

    # Clean up old handlers
    for handler in pip_logger.handlers[:]:
        pip_logger.removeHandler(handler)

    # Use buffer logger
    buffer_handler = logging.StreamHandler(log_buffer)
    buffer_handler.setFormatter(logging.Formatter('%(message)s'))
    pip_logger.addHandler(buffer_handler)

    results = {}

    for pkg in packages:
        pip_logger.info(f"📦 Installing: {pkg}")
        process = subprocess.Popen(
            ["pip", "install", "--upgrade", pkg],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        output_lines = []
        already_satisfied = False

        for line in process.stdout:
            clean_line = line.strip()
            output_lines.append(clean_line)
            pip_logger.info(clean_line)
            if clean_line.startswith("Requirement already satisfied:"):
                already_satisfied = True

        process.wait()

        if already_satisfied:
            status = "skipped"
        elif process.returncode == 0:
            status = "success"
        else:
            status = "failed"

        results[pkg] = {
            "status": status,
            "messages": output_lines
        }

    # 📌 Print clean summary
    for pkg, info in results.items():
        emoji = {"success": "✅", "skipped": "⏭️", "failed": "❌"}[info["status"]]
        print(f"{emoji} {pkg} → {info['status']}")

    # Return both result and captured logs in case needed
    return results, log_buffer.getvalue()



"""
Example Usage 

packages = ["google-auth", "nonexistent-package"]
results, logs = run_pip_install_summary(packages)
print(logs) # if in case want to display logs


# 🧠 Why This Is Better for Jupyter
| Concern                   | Addressed                                 |
| ------------------------- | ----------------------------------------- |
| Duplicate logger handlers | ✅ Removed every time function runs        |
| Log buffer memory growth  | ✅ Re-initialized per call                 |
| Reentrancy / reusability  | ✅ Safe to run in same notebook many times |


"""