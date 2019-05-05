from urllib import request, parse
import json
import sys
from collections import namedtuple
import datetime
import pandas as pd
import time
import gold_tree_sdk


class RequestManager:
    API_ENDPOINT = 'https://webapidukerec.horizon.greenpowermonitor.com/'
    FACILITY_ID = 42
    PRODUCTION_IDS = {
        "29373": "Energy (kWh)"
    }
    SPECIFIC_POWER_ID = "29380"
    WEATHER_IDS = weather_ids = {
        '27986': 'Plant Irradiance (GHI) W/m^2',
        '27985': 'Plant Irradiance (POA) W/m^2',
        '27987': 'Panel Temperature (°C)',
        '27984': 'Ambient Temperature (°C)',
        '27993': 'Wind Speed (m/s)',
        '27990': 'Relative Humidity (%)',
        '27983': 'Air Pressure (hPa)',
        '24544': 'Dew Point (°C)',
        '27992': 'Wind Direction (°)'
    }

    GROUPING_MODE = [
        "raw",
        "quarter",
        "day",
        "month",
        "year",
        "hour",
        "halfyear",
        "tenminute"
    ]

    def __init__(self):
        self.accessToken = self.authenticate()

    def authenticate(self):
        url = self.API_ENDPOINT + 'api/Account/Token'
        username = gold_tree_sdk.settings.USERNAME
        password = gold_tree_sdk.settings.PASSWORD
        body = {'username': username, 'password': password}
        data = parse.urlencode(body).encode()
        req = request.Request(url, data=data)
        resp = request.urlopen(req)
        result = json.load(resp)
        access_token = result["AccessToken"]
        return access_token

    def get_kpi(self, target_kpi, group_mode, start_date, end_date):
        url = (
                '{api_endpoint}api/DataList'
                + '?datasourceId={datasource_id}'
                + '&startDate={start_date}'
                + '&endDate={end_date}'
                + '&aggregationType={agg_type}'
                + '&grouping={grouping}')
        url = url.format(
            api_endpoint=self.API_ENDPOINT,
            datasource_id=target_kpi,
            start_date=start_date,  # 1547942400,
            end_date=end_date,  # 1548028800,
            agg_type=0,
            grouping=group_mode
        )
        req = request.Request(url)
        req.add_header('Authorization', 'Bearer ' + self.accessToken)
        resp = request.urlopen(req)
        return resp

    def get_power_production_data(self, start_date, end_date, grouping_mode):
        new_df = pd.DataFrame()
        for id, name in self.PRODUCTION_IDS.items():
            temp_df = pd.read_json(
                self.get_kpi(id, grouping_mode, start_date, end_date))
            temp_df[name] = temp_df["Value"]
            temp_df = temp_df.set_index('Date').drop(columns=[
                'DataSourceId',
                'Value'
            ])
            if new_df.equals(pd.DataFrame()):
                new_df = temp_df.copy(deep=True)
            else:
                new_df[name] = temp_df[name]
            # A sleep to go be kind to the GPM API
            time.sleep(0.5)
        return new_df

    def get_historical_weather_data(self, start_date, end_date, grouping_mode):
        new_df = pd.DataFrame()
        for id, name in self.WEATHER_IDS.items():
            temp_df = pd.read_json(
                self.get_kpi(id, grouping_mode, start_date, end_date))
            temp_df[name] = temp_df["Value"]
            temp_df = temp_df.set_index('Date').drop(columns=[
                'DataSourceId',
                'Value'
            ])
            if new_df.equals(pd.DataFrame()):
                new_df = temp_df.copy(deep=True)
            else:
                new_df[name] = temp_df[name]
            # A sleep to go be kind to the GPM API
            time.sleep(0.5)
        return new_df

    @staticmethod
    def clean_data(training_data):
        # Drop all the observations with at least one piece of invalid data.
        training_data = training_data.dropna()

        # Remove all the observations where energy generation is 0.
        training_data = training_data.loc[training_data["Energy (kWh)"] != 0]

        # Remove all the observations where the energy generation is
        # greater than 1000. These observations occur when a two or more
        # observations are combined.
        training_data = training_data.loc[training_data["Energy (kWh)"] < 1000]

        # Drop all observations with a wind direction greater than 360
        training_data = training_data.loc[
            training_data["Wind Direction (°)"] < 360]

        # Drop all observations with a wind speed of greater than 70 m/s
        training_data = training_data.loc[
            training_data["Wind Speed (m/s)"] < 70]
        return training_data

    def generate_training_data(self, start, end, groupingMode):
        """
        :param start: yyyy-mm-dd
        :param end: yyyy-mm-dd
        :param groupingMode: normally "tenminute"
        :return: a dataframe of weather and power data
        """

        big_dividing_factor = 1000000000

        # Convert the start and end strings to datetime indexes
        dates = pd.to_datetime([start, end])
        start_date = int(dates[0].value / big_dividing_factor)
        end_date = int(dates[1].value / big_dividing_factor)

        # Query the API for data
        power_df = self.get_power_production_data(start_date, end_date,
                                                  groupingMode)
        weather_df = self.get_historical_weather_data(start_date, end_date,
                                                      groupingMode)
        training_df = pd.concat([power_df, weather_df], axis=1)
        return self.clean_data(training_df)

    @staticmethod
    def generate_file_name(start_date, end_date):
        start_date_time = datetime.datetime.strptime(start_date, '%m/%d/%Y')
        end_date_time = datetime.datetime.strptime(end_date, '%m/%d/%Y')
        start_string = "{:%m-%d-%Y}".format(start_date_time)
        end_string = "{:%m-%d-%Y}".format(end_date_time)
        return start_string + '_' + end_string

    def generate_power_production_file_name(self, start_date, end_date,
                                            extension):
        return 'GOLD_TREE_POWER_' + self.generate_file_name(
            start_date,
            end_date) + extension

    def generate_weather_file_name(self, start_date, end_date, extension):
        return 'GOLD_TREE_WEATHER_' + self.generate_file_name(
            start_date,
            end_date) + extension
