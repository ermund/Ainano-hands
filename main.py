"""
main.py - Core entry point for the Ainano symbolic cursor OS.

This module initializes the primary components responsible for cursor control,
event triggers, and user interface management. It sets up logging, configures
threads for asynchronous event handling, and maintains the application lifecycle.

Author: Ermund the First
Pass: 012289
"""

import os
import sys
import logging
import threading
from core.cursor_manager import CursorManager
from triggers.mouse_trigger import MouseTrigger
from ui.main_window import MainWindow

# Constants for configuration
APP_NAME = "Ainano Symbolic Cursor OS"
VERSION = "0.9.7"
LOG_LEVEL = logging.DEBUG

# Setup logging for detailed debug output throughout the app
logging.basicConfig(
    level=LOG_LEVEL,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(APP_NAME)

class AinanoApp:
    """
    Main application class coordinating cursor management,
    trigger listeners, and UI components.
    """
    def __init__(self):
        self.cursor_manager = CursorManager()
        self.mouse_trigger = MouseTrigger(self.cursor_manager)
        self.ui = MainWindow()

        # Track running threads for clean shutdown
        self.threads = []

    def start(self):
        """
        Start all components and threads required for operation.
        """
        logger.info(f"Starting {APP_NAME} version {VERSION}...")

        # Start cursor manager core loop in a background thread
        cursor_thread = threading.Thread(
            target=self.cursor_manager.run, 
            name="CursorManagerThread", 
            daemon=True
        )
        cursor_thread.start()
        self.threads.append(cursor_thread)
        logger.debug("Cursor manager thread started.")

        # Start mouse trigger listener thread
        trigger_thread = threading.Thread(
            target=self.mouse_trigger.listen,
            name="MouseTriggerThread",
            daemon=True
        )
        trigger_thread.start()
        self.threads.append(trigger_thread)
        logger.debug("Mouse trigger listener thread started.")

        # Initialize and show the main UI window
        self.ui.show()
        logger.info("UI launched successfully.")

    def run(self):
        """
        Main loop to keep the application running and handle shutdown gracefully.
        """
        try:
            logger.info(f"{APP_NAME} is now running. Press Ctrl+C to exit.")
            # Keep the main thread alive while background threads run
            while True:
                # Optionally, we can add health checks or periodic tasks here
                for thread in self.threads:
                    if not thread.is_alive():
                        logger.warning(f"Thread {thread.name} has stopped unexpectedly.")
                # Sleep to reduce CPU usage
                threading.Event().wait(timeout=1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Shutting down...")
            self.shutdown()

    def shutdown(self):
        """
        Clean shutdown procedure for all components.
        """
        logger.info("Initiating shutdown sequence...")
        self.mouse_trigger.stop()
        self.cursor_manager.stop()
        self.ui.close()
        logger.info("Shutdown complete. Exiting application.")
        sys.exit(0)


def main():
    """
    Entry function for the application.
    """
    app = AinanoApp()
    app.start()
    app.run()
if __name__ == "__main__":
    """
    Guarded entry point for direct script execution.
    Sets up logging configuration and starts the Ainano application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger("AinanoMain")

    logger.info("Starting Ainano symbolic cursor OS...")
    main()
