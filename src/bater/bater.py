"""TODO"""
import sched
import time
from threading import Thread

import attr
import psutil

min_threshold = 50
max_threshold = 80
timeout = 5.0

scheduler = sched.scheduler(time.time)


def is_percentage(instance: attr.s, attribute: attr.Attribute, value) -> None:
    if not 0 <= value <= 100:
        raise ValueError(f'{attribute.name} must be a value between 0 and 100')


@attr.s
class App:
    min_threshold = attr.ib(default=50, validator=[attr.validators.instance_of(int), is_percentage])
    max_threshold = attr.ib(default=80, validator=[attr.validators.instance_of(int), is_percentage])


def check_battery(sc: sched.scheduler, app: App):
    print('Checking the battery status')
    battery = psutil.sensors_battery()

    if app.min_threshold > battery.percent > app.max_threshold:
        print('Alert')
    scheduler.enter(1, 1, check_battery, (sc, app))


def batter_check_loop(app: App):
    scheduler.enter(2, 1, check_battery, (scheduler, app))
    scheduler.run()


def gui(app: App):
    while True:
        app.min_threshold = int(input('min: '))
        app.max_threshold = int(input('max: '))

if __name__ == '__main__':
    app = App()
    check_thread = Thread(target=batter_check_loop, args=(app,))
    gui_thread = Thread(target=gui, args=(app,))
    check_thread.start()
    gui_thread.start()
