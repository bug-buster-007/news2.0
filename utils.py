from datetime import datetime


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
