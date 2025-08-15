import boto3
import os
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

# Valid auth codes
VALID_AUTH_CODES = {"123456", "654321"}

# Mapping from internal status names to DynamoDB IDs
STATUS_ID_MAP = {
    "Emergency Mode": "SC Emergency Mode",
    "Meeting Mode": "FES Meeting Mode"
}


def check_auth_code(code):
    """
    Returns True if the provided auth code is valid.
    """
    if not code:
        logger.info("No auth code provided.")
        return False

    result = code in VALID_AUTH_CODES
    logger.info("Auth code check result for '%s': %s", code, result)
    return result


def get_status(status_type):
    """
    Get current status value from DynamoDB.
    """
    try:
        logger.info("Fetching status override values from DynamoDB.")

        response = table.get_item(Key={"id": status_type})

        status = response.get('Item', {}).get('Status', False)
        logger.info("Determined status for '%s': %s", status_type, status)

        return {"status": status}

    except Exception as e:
        logger.error("Error fetching statusOverride: %s", str(e))
        raise RuntimeError(f"Error fetching statusOverride: {str(e)}")


def change_status(new_status):
    """
    Change status value in DynamoDB.
    """
    try:
        logger.info("Changing status to: %s", new_status)

        if new_status == "Activate SC Emergency Mode":
            updates = {
                "SC Emergency Mode": True,
                "FES Meeting Mode": False
            }
        elif new_status == "Deactivate SC Emergency Mode":
            updates = {
                "SC Emergency Mode": False
            }
        elif new_status == "Activate FES Meeting Mode":
            updates = {
                "SC Emergency Mode": False,
                "FES Meeting Mode": True
            }
        elif new_status == "Deactivate FES Meeting Mode":
            updates = {
                "FES Meeting Mode": False
            }
        else:
            raise ValueError(f"Invalid status value: {new_status}")

        for key, val in updates.items():
            dynamo_id = STATUS_ID_MAP.get(key, key)
            logger.info("Updating DynamoDB item: id=%s, Status=%s", dynamo_id, val)
            table.put_item(Item={"id": dynamo_id, "Status": val})

        logger.info("Status update successful.")
        return {
            "message": f"Status updated: {new_status}",
            **updates
        }

    except Exception as e:
        logger.error("Error updating status: %s", str(e))
        raise RuntimeError(f"Error updating status: {str(e)}")


def lambda_handler(event, context):
    """
    Main Lambda entry point.
    """
    try:
        logger.info("Lambda triggered with event: %s", event)
        params = event.get("Details", {}).get("Parameters", {})

        if "function" in params:
            func = params["function"]
            logger.info("Function requested: %s", func)
            if func == "get_status":
                status_type = params.get("status_type", "")
                return get_status(status_type)
            else:
                raise ValueError(f"Unknown function: {func}")

        elif "change_status" in params:
            new_status = params["change_status"]
            logger.info("Change status request: %s", new_status)
            return change_status(new_status)

        elif "check_auth" in params:
            auth_code = params["check_auth"]
            logger.info("Auth check request for code: %s", auth_code)
            result = check_auth_code(auth_code)
            return {"AuthCodeStatus": result}

        else:
            raise ValueError("Parameters must contain 'function', 'change_status', or 'check_auth'")

    except Exception as e:
        logger.error("Lambda handler error: %s", str(e))
        raise RuntimeError(f"Lambda handler error: {str(e)}")
