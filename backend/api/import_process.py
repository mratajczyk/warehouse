import json
import sys
import threading
import time

import schedule
from loguru import logger

from api.persistence.blob import clear_object, get_object_to_import, read_object
from api.services.inventory import UpdateInventoryException, run_update_inventory

logger.remove()
logger.add(sys.stderr, level="INFO")


def process_heartbeat():
    """Log heartbea
    @TODO - consider checking health of process (database connection, storage connection)
    """
    logger.info("\u2764\uFE0F")


def run_import():
    logger.debug("Start import")
    import_object = get_object_to_import()
    if import_object:
        logger.info("%s - start loading" % import_object.object_name)
        data = read_object(import_object.object_name)
        logger.info(
            "%s - loaded %i bytes" % (import_object.object_name, import_object.size)
        )
        try:
            run_update_inventory(json.loads(data))
            logger.success("%s" % import_object.object_name)
        except UpdateInventoryException:
            logger.exception("%s - import failed" % import_object.object_name)
        clear_object(import_object)
    else:
        logger.debug("Nothing to import")


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


"""
Define process that listens for new files in storage and imports them to the warehouse.

@TODO - consider switching from separate process to a task queue that consumes events when new files are added 
to the bucket (S3 Lambda, Minio Notifications) 
"""
scheduler = schedule.Scheduler()
scheduler.every(15).seconds.do(run_threaded, process_heartbeat)
scheduler.every(1).seconds.do(run_threaded, run_import)

if __name__ == "__main__":
    logger.success("Process started - watching for files to import!")
    while True:
        scheduler.run_pending()
        time.sleep(1)
