#!/usr/bin/env bash
set -euo pipefail
set -a
source "$HOME/.jobbot.env"
set +a
source "$HOME/jobbot/bin/activate"
python "$HOME/job_finder.py"
