#!/bin/bash
#

LOG_DIR="../web_logs"

start_webapp() {
    source venv/bin/activate
    flask run --host=0.0.0.0 --port=8080 > "$LOG_DIR/webapp.log" 2>&1 &
}

stop_webapp() {
    pkill -f "flask run"
}

restart_webapp() {
    stop_webapp
    start_webapp
}

case "$1" in
    start)
        start_webapp
        ;;
    stop)
        stop_webapp
        ;;
    restart)
        restart_webapp
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
