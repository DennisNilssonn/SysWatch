import os
from datetime import datetime


class SysWatchLogger:
    # Hanterar loggning för SysWatch
    # Skapar dagliga loggfiler och skriver direkt till disk

    def __init__(self):
        self.logs_dir = "logs"
        self.setup_logging()

    def setup_logging(self):
        # Sätter upp loggfilen för denna programstart
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.log_filename = os.path.join(self.logs_dir, f"syswatch_{timestamp}.log")

    def _write_log(self, level, message):
        # Skriver loggpost direkt till fil
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {level:<8} | {message}\n"

        try:
            with open(self.log_filename, "a", encoding="utf-8") as f:
                f.write(log_entry)
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            print(f"Fel vid loggning: {e}")

    def _log_info(self, message):
        # Skriver INFO-meddelande
        self._write_log("INFO", message)

    def _log_warning(self, message):
        # Skriver WARNING-meddelande
        self._write_log("WARNING", message)

    def _log_error(self, message):
        # Skriver ERROR-meddelande
        self._write_log("ERROR", message)

    def log_program_start(self):
        # Programstart
        self._log_info("=" * 60)
        self._log_info("SYSWATCH PROGRAM STARTAT")
        self._log_info(f"Starttid: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._log_info("=" * 60)

    def log_program_exit(self):
        # Programavslut
        self._log_info("=" * 60)
        self._log_info("SYSWATCH PROGRAM AVSLUTAT")
        self._log_info(
            f"Avslutningstid: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._log_info("=" * 60)

    def log_user_action(self, action, details=""):
        # Användaråtgärd
        if details:
            self._log_info(f"ANVÄNDARÅTGÄRD: {action} - {details}")
        else:
            self._log_info(f"ANVÄNDARÅTGÄRD: {action}")

    def log_menu_navigation(self, menu_name):
        # Menyval
        self._log_info(f"NAVIGERING: Åtkomst till {menu_name}")

    def log_alarm_created(self, alarm_type, value):
        # Nytt alarm skapat
        self._log_info(
            f"ALARM SKAPAT: {alarm_type.upper()} alarm med tröskelvärde {value}%"
        )

    def log_alarm_deleted(self, alarm_type, value, alarm_id):
        # Alarm borttaget
        self._log_info(
            f"ALARM BORTTAGET: {alarm_type.upper()} alarm (ID: {alarm_id}, värde: {value}%)"
        )

    def log_alarm_triggered(self, alarm_type, value, current_usage):
        # Alarm utlöst
        self._log_warning(
            f"ALARM UTLÖST: {alarm_type.upper()} överstiger {value}% (aktuell: {current_usage:.1f}%)"
        )

    def log_monitoring_start(self):
        # Övervakning startad
        self._log_info("SYSTEMÖVERVAKNING: Startad")

    def log_monitoring_stop(self):
        # Övervakning stoppad
        self._log_info("SYSTEMÖVERVAKNING: Stoppad")

    def log_system_stats(self, cpu_usage, memory_usage, disk_usage):
        # Systemstatistik
        self._log_info(
            f"SYSTEMSTATS: CPU: {cpu_usage:.1f}%, RAM: {memory_usage:.1f}%, DISK: {disk_usage:.1f}%"
        )

    def log_error(self, error_message):
        # Fel
        self._log_error(f"FEL: {error_message}")

    def log_warning(self, warning_message):
        # Varning
        self._log_warning(f"VARNING: {warning_message}")

    def log_input(self, input_text):
        # Användarinput
        self._log_info(f"ANVÄNDARINPUT: '{input_text}'")


# Global logger-instans
syswatch_logger = SysWatchLogger()
