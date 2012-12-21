from apscheduler.scheduler import Scheduler
import requests
import os

DATA_REPOSITORY_URL = os.environ.get(
    'LT_DATA_REPO_URL', "http://localhost:5000")


def start_scheduler():
    sched = Scheduler()

    @sched.interval_schedule(seconds=3)
    def update_rdf_store():
        from members import get_members_from_google, format_members_to_rdf
        members = get_members_from_google()
        graph = format_members_to_rdf(members)
        print "Starting request..."
        try:
            requests.post(
                "/".join([DATA_REPOSITORY_URL, "expand"]),
                data={"data": graph.serialize(format="n3")}
            )
        except Exception, e:
            print e
        print "Done."

    sched.configure()
    sched.start()
    return sched

if __name__ == "__main__":
    import signal
    import sys
    print "Starting scheduler..."
    sched = start_scheduler()

    def signal_handler(signal, frame):
            print '\nShutting down scheduler...'
            sched.shutdown()
            sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
