import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import time
from screen_time_app import main  # Import the main function from your backend script

class ScreenTimeService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ScreenTimeService"
    _svc_display_name_ = "Screen Time Tracking Service"
    _svc_description_ = "Service to track screen time and application usage."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._setup_logger()
        self.is_running = True

    def _setup_logger(self):
        logger = logging.getLogger('ScreenTimeService')
        handler = logging.FileHandler('service.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def SvcStop(self):
        self.logger.info('Service is stopping...')
        self.is_running = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.logger.info('Service is starting...')
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        while self.is_running:
            try:
                main()  # Call the main function from your backend script
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in tracking: {e}")
                self.is_running = False

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ScreenTimeService)
