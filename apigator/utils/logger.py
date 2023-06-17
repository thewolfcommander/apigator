import json
import logging
import traceback

def log_info(info_code, data=None, show_data=False):
    # Load custom infos
    with open('info.json') as f:
        custom_infos = json.load(f)

    # Get the logger
    logger = logging.getLogger(__name__)

    # Log the info message corresponding to the info code
    message = f"""
    ------------------------ LOGGING INFO START ------------------------------
    {info_code}: {custom_infos.get(info_code, 'Unknown info code')}
    """

    if show_data:
        message += f'| DATA: {json.dumps(data)}'

    message += """------------------------ LOGGING INFO END ------------------------------"""
    logger.debug(message)


def log_custom_error(error_code, exception, data=None):
    # Load custom errors
    with open('errors.json') as f:
        custom_errors = json.load(f)

    # Get the logger
    logger = logging.getLogger(__name__)

    # Get the traceback
    tb = traceback.format_exception(type(exception), exception, exception.__traceback__)

    # Log the error message corresponding to the error code
    message = f"""
    ############################### LOGGING ERROR START ###############################\n\n
    {error_code}: {custom_errors.get(error_code, 'Unknown error code')}\n{tb}\n\n
    ############################### LOGGING ERROR END #################################
    """

    logger.debug(message)

    # Prepare response
    response = {
        'status': False,
        'error_code': error_code,
        'message': custom_errors.get(error_code, 'Unknown error code'),
    }

    # Include data in the response if it's provided
    if data is not None:
        response['data'] = data

    return response
