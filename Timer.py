from threading import Thread


class PerpetualTimer(Thread):
    """
    Execute a function periodically.

    Args:
        func: Function/Method that will be invoked
        time: Amount of time
        time_unit: Time unit used in [time].
                Options: secs, mins, hours. Default: secs
        stop_event[Optional]: Event to stop the timer
    """

    def __init__(self, func, time, time_unit="secs", stop_event=None):
        Thread.__init__(self)
        self.func = func
        self.time = time
        self.time_unit = time_unit
        self.stop_event = stop_event

    def run(self):
        if self.time_unit == "secs":
            time_aux = float(self.time)
        elif self.time_unit == "mins":
            time_aux = self.time * 60.0
        elif self.time_unit == "hours":
            time_aux = self.time * 3600.0

        while not self.stop_event.wait(time_aux):
            self.func()
        return
