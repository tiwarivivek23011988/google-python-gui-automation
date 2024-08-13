import threading


class WebDriverProcessManager:
    _instance = None
    _thread_local = threading.local()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebDriverProcessManager, cls).__new__(cls)
            cls._instance.processes = []
        return cls._instance

    @staticmethod
    def get_instance():
        """Get the singleton instance of WebDriverProcessManager."""
        return WebDriverProcessManager()

    def add_process(self, driver):
        """Add a WebDriver instance to the manager."""
        if driver:
            if not hasattr(self._thread_local, 'processes'):
                self._thread_local.processes = []
            self._thread_local.processes.append(driver)

    def cleanup(self):
        """Cleanup all tracked WebDriver processes."""
        processes = getattr(self._thread_local, 'processes', [])
        for driver in processes:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error quitting WebDriver process: {e}")
        # Clear the thread-local processes after cleanup
        self._thread_local.processes = []