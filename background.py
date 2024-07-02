import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyService"
    _svc_display_name_ = "My Python Service"
    _svc_description_ = "This is a sample Python service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

        # Setup logging
        log_file_path = 'C:\\PycharmProjects\\Screen-Timer-Productivity-App\\logfile.log'
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger()
        self.logger.info("Service initialized.")

    def SvcStop(self):
        self.logger.info("Service stop signal received.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.logger.info("Service is starting.")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        try:
            from application_logic import ScreenTimeApp
            self.logger.info("Main method started.")
            screen_time_app = ScreenTimeApp()
            screen_time_app.run()

            while True:
                self.logger.info("Running ScreenTimeApp.")
                self.logger.info("Background task running...")
                win32event.WaitForSingleObject(self.hWaitStop, 5000)

        except ImportError as e:
            self.logger.error(f"ImportError in main: {e}")
            raise

        except Exception as e:
            self.logger.error(f"Exception in main: {e}")
            raise


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
