import logging
import os
import re
from datetime import datetime, timedelta
from mimetypes import guess_extension

import requests
from dateutil.relativedelta import relativedelta


def get_previous_nth_month(no_of_months: int) -> tuple:
    '''
    Calculate the month and year after subtracting a
        given number of months from the current month.

    Args:
        no_of_months (int): The number of months to subtract
            from the current month.

    Returns:
        tuple: A tuple containing the target month (int)
        and the target year (int).

    Example:
        If the current month is July 2024 and no_of_months is 15,
        the function will return (4, 2023) which represents April 2023.
    '''
    # Get the current date
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Calculate the target month by subtracting the given number of months
    target_month = current_month - no_of_months

    # Adjust the year if the resulting month is less than or equal to zero
    if target_month <= 0:
        years_to_subtract = (abs(target_month) // 12) + 1
        target_year = current_year - years_to_subtract
        target_month += 12 * years_to_subtract
    else:
        target_year = current_year

    return target_month, target_year


def calculate_past_date(time_period: str) -> datetime:
    '''
    Method takes time ago and return respective date at that time
    '''
    pattern = r'(\d+)\s*(hour|day|minute|second|week|month|year)s?\s*ago'
    match = re.match(pattern, time_period, re.IGNORECASE)

    if not match:
        raise ValueError(
            "Invalid time format. Expected format: '<number> <unit> ago'.",
        )

    amount, unit = match.groups()
    amount = int(amount)

    now = datetime.now()

    # Map units to appropriate timedelta or relativedelta arguments
    if unit in {'hour', 'day', 'minute', 'second', 'week'}:
        kwargs = {unit + 's': amount}
        past_date = now - timedelta(**kwargs)
    elif unit in {'month', 'year'}:
        kwargs = {unit + 's': amount}
        past_date = now - relativedelta(**kwargs)
    else:
        raise ValueError(f'Unsupported time unit: {unit}')

    return past_date.strftime('%b %d, %Y')


def download_image(url: str, file_path: str):
    '''
    Download an image from a URL
    and save it to a file with a dynamic extension.

    :param url: The URL of the image to download.
    :param file_path: The path where the image will be saved.
    '''
    try:
        # Send a GET request to the image URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Determine the MIME type and file extension
        content_type = response.headers.get('Content-Type')
        if content_type:
            extension = guess_extension(content_type.split(';')[0])
            if extension:
                file_path_with_ext = f"{file_path}{extension}"
            else:
                file_path_with_ext = file_path
        else:
            file_path_with_ext = file_path

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname('output/news_images/'), exist_ok=True)

        # Write the image content to the file path
        with open(file_path_with_ext, 'wb') as file:
            file.write(response.content)
        logging.info(f'Image downloaded and saved to {file_path}')

    except requests.RequestException as e:
        logging.error(f'An error occurred while downloading the image: {e}')
