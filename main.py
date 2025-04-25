################################################################################
################################################################################
import requests
import json
import schedule
import time
import logging
import logging.config
from datetime import date

import config

################################################################################
# Main variables
################################################################################
INSTANCE_ID = config.INSTANCE_ID
VULTR_API_KEY = config.VULTR_API_KEY
TOKEN = config.TOKEN
GROUP_CHAT_ID = config.CHAT_ID
VPSFLAG = config.VPSFLAG

VULTR_URL = "https://api.vultr.com/v2/instances/"+INSTANCE_ID+"/bandwidth"
TELEGRAM_BOT_API = "https://api.telegram.org/bot"
TELEGRAM_BOT_API_SEND_MESSAGE_METHOD = "/sendMessage?"

SCHEDULED_TASK_DELAY = 60  # Sec

logger = logging.getLogger('main_logging')

################################################################################
# Functions
################################################################################
################################################################################
# name:        send_2_telegram
# description: 
################################################################################
def send_2_telegram(chat_id, message):
    """

    """
    url = TELEGRAM_BOT_API + TOKEN + TELEGRAM_BOT_API_SEND_MESSAGE_METHOD + "chat_id=" + chat_id
    r = requests.post(url, data={'text': {message}, 'disable_notification' : 'true'})
    logger.info('{0:s} {1:s}'.format("send_2_telegram: result:", r.text))

################################################################################
# name:        get_bandwidth
# description: 
################################################################################
def get_bandwidth():
    """

    """
    response = requests.get(VULTR_URL, headers={'Authorization': 'Bearer %s' % VULTR_API_KEY})

    incoming_bytes = 0
    outgoing_bytes = 0
    days = 0

    if response.status_code == 200:
        bandwidth_json = response.json()
        bandwidth_dates = bandwidth_json['bandwidth']

        today = date.today()
        day = today.strftime("%Y-%m-%d")

        for key,value in bandwidth_dates.items():
            if key[0:8] == day[0:8]:
                incoming_bytes = incoming_bytes + (value.get("incoming_bytes"))/(1024 * 1024 * 1024)
                outgoing_bytes = outgoing_bytes + (value.get("outgoing_bytes"))/(1024 * 1024 * 1024)
                days += 1

    str = 'Days: {0:d} In: {1:.2f} Out: {2:.2f}'.format(days, round(incoming_bytes, 2), round(outgoing_bytes, 2))
    logger.info('{0:s} {1:s}'.format("get_bandwidth:", str))
    return str

################################################################################
# name:        update_info
# description: 
################################################################################
def update_info():
    """

    """
    str = get_bandwidth()
    send_2_telegram(GROUP_CHAT_ID, f'{VPSFLAG}: {str}')

################################################################################
# name:        scheduled_task
# description: Task for scheduled routine
################################################################################
def scheduled_task():
    """
    Scheduled task
    """
    schedule.every().day.at('06:00').do(update_info)
    logger.info("scheduled_task: Start")
    while True:
        logger.info("scheduled_task: while")
        schedule.run_pending()
        time.sleep(SCHEDULED_TASK_DELAY)

################################################################################
# Main
################################################################################
def main():
    """
    Main
    """
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.basicConfig(filename='log.log')
    logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(encoding='utf-8')

    logger.setLevel(logging.DEBUG)
    logger.info("Starting VULTRAPI BOT")
    scheduled_task()


if __name__ == "__main__":
    main()
