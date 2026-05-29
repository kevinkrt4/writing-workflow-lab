#!/bin/zsh

# --------------------------------------------------------------------
# Writers Workbench Launcher
#
# Syntax:
#
#   start_workbench.sh start
#   start_workbench.sh stop
#   start_workbench.sh status
# --------------------------------------------------------------------

APP_DIR="$HOME/GitHub/writers_workbench"
VENV="$HOME/.venvs/prompts_env/bin/activate"

PORT="5050"
URL="http://127.0.0.1:$PORT"

PID_PATTERN="python.*app.py"

# --------------------------------------------------------------------
# Cleanup Handler
# --------------------------------------------------------------------

cleanup() {

    echo
    echo "Stopping Writers Workbench..."

    if [[ -n "$FLASK_PID" ]]; then
        kill "$FLASK_PID" 2>/dev/null
        wait "$FLASK_PID" 2>/dev/null
    fi

    exit 0
}

trap cleanup INT TERM

# --------------------------------------------------------------------
# Start Writers Workbench
# --------------------------------------------------------------------

start_app() {

    cd "$APP_DIR" || exit 1

    source "$VENV"

    # Prevent duplicate launches
    if lsof -i :"$PORT" | grep -q Python; then
        echo "Writers Workbench already running at $URL"
        open -a Safari "$URL"
        exit 0
    fi

    echo "Starting Writers Workbench..."

    # Suppress known Python 3.14 semaphore cleanup warning
    PYTHONWARNINGS="ignore:resource_tracker:UserWarning" python app.py &
    FLASK_PID=$!

    # Give Flask time to initialize
    sleep 2

    # Open browser
    open -a Safari "$URL"

    # Keep launcher attached to Flask lifecycle
    wait "$FLASK_PID"
}

# --------------------------------------------------------------------
# Stop Writers Workbench
# --------------------------------------------------------------------

stop_app() {

    echo "Stopping Writers Workbench..."

    pkill -f "$PID_PATTERN" 2>/dev/null

    echo "Stopped."
}

# --------------------------------------------------------------------
# Show Status
# --------------------------------------------------------------------

status_app() {

    if lsof -i :"$PORT" | grep -q Python; then
        echo "Writers Workbench is running at $URL"
    else
        echo "Writers Workbench is not running."
    fi
}

# --------------------------------------------------------------------
# Command Dispatcher
# --------------------------------------------------------------------

case "$1" in

    start)
        start_app
        ;;

    stop)
        stop_app
        ;;

    status)
        status_app
        ;;

    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;

esac
