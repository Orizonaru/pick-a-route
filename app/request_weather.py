from typing import List, Dict, Union
from default_requests_processing import DefaultRequestsProcessing

class RequestWeather(DefaultRequestsProcessing):
    possible_forecast_days = {1, 5, 10, 15}

    def __init__(self, api_token: str, language: str):
        super().__init__(api_url="http://dataservice.accuweather.com")
        self.api_token = api_token
        self.language = language

    def fetch_city_autocomplete(self, city_name: str) -> List[Dict]:
        query_params = {
            "q": city_name,
            "language": self.language,
            "apikey": self.api_token
        }
        response = self.fetch(endpoint="locations/v1/cities/autocomplete", query_params=query_params)
        return response

    def fetch_daily_forecast(
        self, forecast_days: int, location_id: str, include_details: bool = True, use_metric: bool = True
    ) -> Union[Dict, None]:

        if forecast_days not in self.possible_forecast_days:
            raise ValueError(
                f"Некорректное значение для параметра 'forecast_days': {forecast_days}. "
                f"Допустимые значения: {self.possible_forecast_days}."
            )

        query_params = {
            "language": self.language,
            "details": include_details,
            "metric": use_metric,
            "apikey": self.api_token
        }

        endpoint = f"forecasts/v1/daily/{forecast_days}day/{location_id}"
        response = self.fetch(endpoint=endpoint, query_params=query_params)

        for daily_forecast in response.get("DailyForecasts", []):
            day_info = {
                "date": daily_forecast["Date"],
                "max_temperature": daily_forecast["Temperature"]["Maximum"]["Value"],
                "min_temperature": daily_forecast["Temperature"]["Minimum"]["Value"],
                "wind_speed": daily_forecast["Day"]["Wind"]["Speed"]["Value"],
                "rain_chance": daily_forecast["Day"]["PrecipitationProbability"],
            }
            daily_forecast_data = [day_info]

        return daily_forecast_data