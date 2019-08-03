import datetime
import logging
import os

filename = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

if not os.path.exists("../logs"):
    os.mkdir("../logs")

logging.basicConfig(filename="../logs/{}.log".format(filename),
                    format='%(message)s',
                    level=logging.INFO)

logger = logging.getLogger("ShowdownBot")
