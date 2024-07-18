'''
This module contains all excel file handling
'''

import uuid

from RPA.Excel.Files import Files

from constants import DOLLAR_KEYWORDS
from utils import calculate_past_date, download_image


class ExcelFile:
    '''
    Class has all methods and attributes related to excel file
    Excel file created once news are extracted
    '''

    def __init__(self, file_name: str = 'news_list') -> None:
        self._file = Files()
        self._file_name = file_name
        self._output_file = f'output/{self._file_name}.xlsx'

        # Open or create the Excel file
        self._file.create_workbook(self._output_file)

    @property
    def file(self) -> Files:
        return self._file

    def save_data(self, data: list = []) -> None:

        # Write headers to the first row if needed
        headers = [
            'Title',
            'Date',
            'Description',
            'Image',
            'Phrase Count',
            'Has Amount',
        ]
        self._file.append_rows_to_worksheet([headers])

        # Write each news item to the Excel file
        for news in data:

            time_period = ExcelFile._find_date(news[0])
            title = news[1].replace('...', '')
            description = news[2].replace('...', '')
            picture_file = str(uuid.uuid4())[:8]
            phrase_count = news[3]
            has_amount = ExcelFile._contains_dollar_keywords(
                title,
                description,
            )
            image_url = news[4]
            download_image(image_url, f'output/news_images/{picture_file}')
            self._file.append_rows_to_worksheet(
                [
                    (
                        title,
                        time_period,
                        description,
                        f'{picture_file}.jpg',
                        phrase_count,
                        str(has_amount),
                    )
                ]
            )

        # Save the Excel file
        self._file.save_workbook(self._output_file)
        self._file.close_workbook()

    @staticmethod
    def _contains_dollar_keywords(*texts) -> bool:
        # Convert keywords to lowercase
        keywords = {keyword.lower() for keyword in DOLLAR_KEYWORDS}

        return any(
            keyword in text.lower() for text in texts for keyword in keywords
        )  # check for any keyword presence

    @staticmethod
    def _find_date(time_period: str) -> str:
        '''
        Function takes time period as parameter and return date
        '''

        if 'ago' in time_period:
            return calculate_past_date(time_period)

        return time_period
