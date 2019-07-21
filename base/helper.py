from datetime import timedelta
from django.utils import timezone


class TimeHelper(object):
    """ Helper class for time related functions.
    """

    @staticmethod
    def __get_seconds(time_value, time_unit):
        """ Returns the `seconds` corresponding to given number of time units.
        :param time_value: integer
        :param time_unit: `weeks` / `days` / `hours` / `minutes`
        :return: integer
        """

        return {
            "weeks": 604800,
            "days": 86400,
            "hours": 3600,
            "minutes": 60
        }.get(time_unit) * time_value

    @staticmethod
    def calculate_future_time(
            time_value, time_unit, from_time=timezone.now()):
        """ Return's future time basis the given time and delta.
        :param time_value: integer
        :param time_unit: `weeks` / `days` / `hours` / `minutes`
        :param from_time: `time`
        :return: `time`
        """

        seconds = TimeHelper.__get_seconds(time_value, time_unit)
        return from_time + timedelta(seconds=seconds)
