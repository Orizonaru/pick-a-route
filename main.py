import logging
import requests
from app.request_weather import RequestWeather
import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

api_key = 'qiLNhPlYwsQwGIOAdSB8XbXOD1m1tQGE'

app.layout = dbc.Container([
    html.H1('Pick-a-route', className='my-3'),
    dbc.Row([
        dbc.Col([
            dcc.Input(
                id="start_city_input".format('text'),
                type='text',
                placeholder="Город отправления".format('text'),
                className='form-control',

            ),
        ], md=5),
        dbc.Col([
            dbc.Input(
                id="end_city_input".format('text'),
                type='text',
                placeholder="Город прибытия".format('text'),
                className='form-control',

            )
        ], md=5),
        dbc.Col([
            html.Button('Узнать погоду',
                        id='submit_button',
                        className='btn btn-dark w-100',
                        n_clicks=0)
        ], md=2)
    ], className='my-3'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Погода в городе отправления', id='start_city_header'),
                dbc.CardBody([
                    html.P('First string', id='start_city_temp', className='card-text'),
                    html.P('Second string', id='start_city_wind_speed', className='card-text'),
                    html.P('Third string', id='start_city_rain_prob', className='card-text'),
                    html.P('Third string', id='start_city_isgood', className='card-text'),
                ])
            ], id='start_city_card', style={'display': 'none'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Погода в городе прибытия', id='end_city_header'),
                dbc.CardBody([
                    html.P('First string', id='end_city_temp', className='card-text'),
                    html.P('Second string', id='end_city_wind_speed', className='card-text'),
                    html.P('Third string', id='end_city_rain_prob', className='card-text'),
                    html.P('Third string', id='end_city_isgood', className='card-text'),
                ])
            ], id='end_city_card', style={'display': 'none'})
        ], md=6)
    ]),
])

@app.callback(
    [
     Output('start_city_card', 'style'),
     Output('start_city_header', 'children'),
     Output('start_city_temp', 'children'),
     Output('start_city_wind_speed', 'children'),
     Output('start_city_rain_prob', 'children'),
     Output('start_city_isgood', 'children'),
     Output('end_city_card', 'style'),
     Output('end_city_header', 'children'),
     Output('end_city_temp', 'children'),
     Output('end_city_wind_speed', 'children'),
     Output('end_city_rain_prob', 'children'),
     Output('end_city_isgood', 'children'),],
    [Input('start_city_input', 'value'),
     Input('end_city_input', 'value'),
     Input('submit_button', 'n_clicks')]
)
def action(start_city, end_city, n_clicks):
    if ctx.triggered_id == 'submit_button':
        #if not start_city or not end_city:
        #    return jsonify({"error": "Не указаны оба города"}), 400

        def weather_validation(temp_max, temp_min, wind_speed, rain_prob):
            if temp_max > 35 or temp_min < -10 or wind_speed > 50 or rain_prob > 80:
                return False
            else:
                return True

        weather_client = RequestWeather(api_key=api_key, language="ru-ru")

        def get_city_weather(city_name):
            autocomplete_results = weather_client.fetch_city_autocomplete(city_name)
            if not autocomplete_results:
                return None
            location_code = autocomplete_results[0]["Key"]
            forecast = weather_client.fetch_daily_forecast(forecast_days=1, location_code=location_code)[0]
            return {
                "name": city_name,
                "temp_max": forecast["temp_max"],
                "temp_min": forecast["temp_min"],
                "wind_speed": forecast["wind_speed"],
                "rain_prob": forecast["rain_prob"],
                "is_good": weather_validation(forecast["temp_max"], forecast["temp_min"], forecast["wind_speed"],
                                              forecast["rain_prob"])
            }

        start_city_data = get_city_weather(start_city)
        end_city_data = get_city_weather(end_city)

        #if not start_city_data or not end_city_data:
        #    return jsonify({"error": "Не удалось получить данные для одного из городов"}), 500

        return (
                {'display': 'block'},
                start_city,
                f'Температура от {start_city_data['temp_min']} до {start_city_data['temp_max']}',
                f'Скорость ветра {start_city_data['wind_speed']} м/с',
                f'Вероятность дождя {start_city_data['rain_prob']}%',
                f'Погода благоприятная' if start_city_data['is_good'] else f'Ехать не стоит',
                {'display': 'block'},
                end_city,
                f'Температура от {end_city_data['temp_min']} до {end_city_data['temp_max']}',
                f'Скорость ветра {end_city_data['wind_speed']} м/с',
                f'Вероятность дождя {end_city_data['rain_prob']}%',
                f'Погода благоприятная' if end_city_data['is_good'] else f'Ехать не стоит'
                )


    else:
        return (
                {'display': 'none'},
                'Город отправления',
                'Температура',
                'Скорость ветра',
                'Вероятность дождя',
                'Рекомендация',
                {'display': 'none'},
                'Город прибытия',
                'Температура',
                'Скорость ветра',
                'Вероятность дождя',
                'Рекомендация'
                )


if __name__ == '__main__':
    app.run_server(debug=True)