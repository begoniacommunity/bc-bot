from main import scheduler


class SchedulerManager:
    def __init__(self):
        self.scheduler = scheduler
        self.started = False

    def start(self):
        if not self.started:
            self.scheduler.start()
            self.started = True

    def add_job(self, *args, **kwargs):
        self.start()
        return self.scheduler.add_job(*args, **kwargs)


main_sched = SchedulerManager()
