#!/usr/bin/env python3
"""
deploy.py — Git commit and push logic for DoomsdayWatch.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

import os
import subprocess


def deploy_changes(state, auto_git=True):
    """Commit and push changes to GitHub Pages.

    Only commits/pushes when auto_git is True (or NUKE_WATCH_AUTO_GIT=1).

    Args:
        state: Current state dict (used for commit message timestamp).
        auto_git: If False, skips git operations entirely.

    Returns:
        dict with keys: committed (bool), pushed (bool), message (str)
    """
    if not auto_git and os.environ.get("NUKE_WATCH_AUTO_GIT") != "1":
        print("Skipped git commit/push (set NUKE_WATCH_AUTO_GIT=1 to enable).")
        return {"committed": False, "pushed": False, "message": "Skipped"}

    result = {"committed": False, "pushed": False, "message": ""}

    try:
        # Configure git identity
        subprocess.run(
            ["git", "config", "user.name", "VoltaIntel"],
            check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "cryptocybrog1337@proton.me"],
            check=True
        )

        # Force-add data files (gitignored but needed on GitHub Pages)
        subprocess.run(
            [
                "git", "add", "-f",
                "data/current_state.json",
                "data/signal_timeline.json",
                "data/predictions/",
                "data/energy_prices.json",
                "data/flight_tracking.json",
            ],
            check=False
        )

        # Stage all changes
        subprocess.run(["git", "add", "-A"], check=True)

        # Commit
        commit_msg = f"Update {state.get('last_updated', '')} — automated"
        r = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True
        )
        if r.returncode == 0:
            print("Committed")
            result["committed"] = True
            result["message"] = "Committed"
        else:
            print("No changes to commit")
            result["message"] = "No changes to commit"
            return result

        # Push
        r = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True,
            text=True
        )
        if r.returncode == 0:
            print("Pushed!")
            result["pushed"] = True
            result["message"] = "Pushed!"
        else:
            err = r.stderr.strip()
            print(err)
            result["message"] = err

    except subprocess.CalledProcessError as e:
        err_msg = f"Git error: {e}"
        print(err_msg)
        result["message"] = err_msg

    return result
