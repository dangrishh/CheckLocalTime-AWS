import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_current_date_gmt_plus_10():
    try:
        now_utc = datetime.utcnow()
        now_gmt_plus_10 = now_utc + timedelta(hours=10)
        current_date = now_gmt_plus_10.date()
        logger.info(f"Current date in GMT+10: {current_date}")
        return current_date
    except Exception as e:
        logger.exception("Error occurred while calculating current date in GMT+10")
        raise

def business_closing_time():
    try:
        now_utc = datetime.utcnow()
        now_gmt_plus_10 = now_utc + timedelta(hours=10)

        cutoff_str = os.environ["BUSINESS_CUTOFF_TIME"]
        cutoff_time_obj = datetime.strptime(cutoff_str, "%H:%M")
        cutoff_time = cutoff_time_obj.time()
        
        cutoff_display = cutoff_time_obj.strftime("%I:%M %p")
        result = now_gmt_plus_10.time() > cutoff_time
        logger.info(f"Is time after {cutoff_display} GMT+10? {result}")
        return result
    except Exception as e:
        logger.exception(f"Error occurred while checking time against {cutoff_display}")
        raise

def lambda_handler(event, context):
    try:
        logger.info("Lambda function started")
        date_today = get_current_date_gmt_plus_10()
        business_closing_time_result = business_closing_time()
        logger.info(f"Processed date: {date_today}, After 4:30 PM: {business_closing_time_result}")
        return {
            'date': str(date_today),
            'BusinessClosingTime': business_closing_time_result
        }
    except Exception as e:
        logger.exception("Unhandled exception in lambda_handler")
        raise
