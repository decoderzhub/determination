import syslog
from threading import Timer
import traceback

class RepeatedTimer(object):
    def __init__(self, first_interval, interval, func, *args, **kwargs):
        self.timer      = None
        self.first_interval = first_interval
        self.interval   = interval
        self.func   = func
        self.args       = args
        self.kwargs     = kwargs
        self.running = False
        self.is_started = False

    def first_start(self):
        try:
            # no race-condition here because only control thread will call this method
            # if already started will not start again
            if not self.is_started:
                self.is_started = True
                self.timer = Timer(self.first_interval, self.run)
                self.running = True
                self.timer.start()
                self.timer.join()

        except Exception as e:
            print(syslog.LOG_ERR, "timer first_start failed %s %s"%(e.message, traceback.format_exc()))
            raise

    def run(self):
        # if not stopped start again
        if self.running:
            self.timer = Timer(self.interval, self.run)
            self.timer.start()
            self.timer.join()
            self.func(*self.args, **self.kwargs)

    def stop(self):
        # cancel current timer in case failed it's still OK
        # if already stopped doesn't matter to stop again
        if self.timer:
            self.timer.cancel()
            self.running = False

