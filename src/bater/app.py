"""TODO"""
import random
from collections import namedtuple
from threading import Thread, Event, Timer, RLock

import attr

from src.bater.validators import is_percentage, is_positive


@attr.s
class App:
    """TODO"""

    min_threshold = attr.ib(
        default=50, validator=[attr.validators.instance_of(int), is_percentage]
    )
    max_threshold = attr.ib(
        default=80, validator=[attr.validators.instance_of(int), is_percentage]
    )
    timeout = attr.ib(
        default=5, validator=[attr.validators.instance_of(float), is_positive]
    )
    _monitor_thread = attr.ib(
        init=False,
        default=attr.Factory(
            lambda self: Thread(target=self.run_battery_monitor, name="battery_monitor"),
            takes_self=True,
        ),
    )
    _gui_thread = attr.ib(
        init=False,
        default=attr.Factory(
            lambda self: Thread(target=self.run_gui_thread, name="gui"), takes_self=True
        ),
    )
    _settings_has_changed: Event = attr.ib(factory=Event, init=False)
    _lock = attr.ib(factory=RLock, init=False)

    def start_battery_monitor(self) -> None:
        """TODO"""
        self._monitor_thread.start()

    def start_gui(self) -> None:
        """TODO"""
        self._gui_thread.start()

    def run_battery_monitor(self) -> None:
        """TODO"""
        print("Checking the battery status")
        Battery = namedtuple("Battery", "percent")
        battery = Battery(random.randint(0, 100))

        with self._lock:
            if not app.min_threshold <= battery.percent <= app.max_threshold:
                print(
                    f"Alert {battery.percent}% is not between {app.min_threshold}%"
                    f" and {app.max_threshold}%"
                )

        Timer(self.timeout, self.run_battery_monitor).start()

    def run_gui_thread(self) -> None:
        """TODO"""
        while True:
            try:
                app.min_threshold = int(input("min: "))
                app.max_threshold = int(input("max: "))
            except (TypeError, ValueError):
                print("Invalid value.")


if __name__ == "__main__":
    app = App()
    app.start_gui()
    app.start_battery_monitor()
