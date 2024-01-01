import json
from libs.logger import logger
import random

class CodingTasksParser:
    """A class to parse coding tasks from a JSON file."""

    def __init__(self):
        """Initialize the parser with the file path."""
        self.file_path = 'data/coding_tasks.json'
        self._data = None
        self._parse()

    def _parse(self):
        """Parse the JSON file and store the data."""
        try:
            with open(self.file_path, 'r') as f:
                self._data = json.load(f)
            logger.info(f'Successfully parsed file {self.file_path}')
        except Exception as exception:
            logger.error(f'Failed to parse file {self.file_path}: {exception}')
            raise

    def _get_tasks(self):
        """Return a list of all tasks."""
        if self._data is None:
            raise ValueError('No data parsed yet')
        return self._data['coding_tasks']

    def _get_task(self, index):
        """Return a specific task by its index."""
        if self._data is None:
            raise ValueError('No data parsed yet')
        try:
            return self._data['coding_tasks'][index]
        except IndexError:
            logger.error(f'No task at index {index}')
            raise

    def get_random_task(self):
        """Return a random task."""
        try:
            tasks = self._get_tasks()
            task = self._get_task(random.randint(0, len(tasks) - 1))
            return task['task'], task['example']['input'], task['example']['output']
        except Exception as exception:
            logger.error(f'Failed to get random task: {exception}')
            raise