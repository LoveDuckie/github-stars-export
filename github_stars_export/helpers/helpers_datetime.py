def get_time_formatted() -> str:
    """
    Get the formatted time stamp
    :return: Returns the formatted time stamp
    """
    from datetime import datetime

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as dd-MM-YYYY_HHmmss
    formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H%M%S")
    return formatted_datetime

