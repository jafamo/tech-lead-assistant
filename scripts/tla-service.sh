#!/usr/bin/env bash
# Instala y gestiona TLA como servicio systemd de usuario.
# Uso: ./scripts/tla-service.sh [install|start|stop|status|logs|uninstall]
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_NAME="tla"
SERVICE_FILE="$HOME/.config/systemd/user/${SERVICE_NAME}.service"
VENV="$PROJECT_DIR/.venv"

_check_venv() {
  if [ ! -f "$VENV/bin/python" ]; then
    echo "Error: entorno virtual no encontrado en $VENV"
    echo "Ejecuta: python3 -m venv .venv && source .venv/bin/activate && pip install -e ."
    exit 1
  fi
}

cmd_install() {
  _check_venv
  mkdir -p "$(dirname "$SERVICE_FILE")"
  cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Tech Lead Assistant
After=network.target

[Service]
Type=simple
WorkingDirectory=${PROJECT_DIR}
ExecStart=${VENV}/bin/python -m tla
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF
  systemctl --user daemon-reload
  systemctl --user enable "$SERVICE_NAME"
  echo "Servicio instalado. Usa '$0 start' para arrancarlo."
}

cmd_start()     { systemctl --user start   "$SERVICE_NAME"; echo "Iniciado."; }
cmd_stop()      { systemctl --user stop    "$SERVICE_NAME"; echo "Detenido."; }
cmd_status()    { systemctl --user status  "$SERVICE_NAME"; }
cmd_logs()      { journalctl --user -u "$SERVICE_NAME" -f; }
cmd_uninstall() {
  systemctl --user stop    "$SERVICE_NAME" 2>/dev/null || true
  systemctl --user disable "$SERVICE_NAME" 2>/dev/null || true
  rm -f "$SERVICE_FILE"
  systemctl --user daemon-reload
  echo "Servicio eliminado."
}

case "${1:-}" in
  install)   cmd_install   ;;
  start)     cmd_start     ;;
  stop)      cmd_stop      ;;
  status)    cmd_status    ;;
  logs)      cmd_logs      ;;
  uninstall) cmd_uninstall ;;
  *)
    echo "Uso: $0 [install|start|stop|status|logs|uninstall]"
    echo ""
    echo "  install    Registra TLA como servicio systemd de usuario"
    echo "  start      Arranca el servicio"
    echo "  stop       Para el servicio"
    echo "  status     Muestra el estado"
    echo "  logs       Sigue los logs en tiempo real"
    echo "  uninstall  Elimina el servicio"
    exit 1
    ;;
esac
