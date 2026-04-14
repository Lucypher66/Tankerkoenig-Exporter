import logic
import yaml
from flask import Flask, render_template, Response

with open("config.yml") as config:
    config_data = yaml.safe_load(config)
config.close()

app = Flask(__name__)

if bool(config_data['config']['enable_index_page']) != False:
    @app.route('/',methods=["GET"])
    def index_page():
        return render_template("index.html")

if bool(config_data['config']['enable_config_page']) != False:
    @app.route('/config',methods=["GET"])
    def config_page():
        return config_data

if bool(config_data['config']['enable_metrics_page']) != False:
    @app.route('/metrics', methods=["GET"])
    def metrics_page():
        metrics_output = ""
        stations = config_data["config"]["station_ids"]

        for station in stations:
            request = logic.build_request(
                station,
                api_key=config_data["config"]["api_key"]
            )
            data = logic.request_data(request)

            station_name = logic.prometheus_escape(data["station"]["name"])
            is_open = 1 if data["station"]["isOpen"] else 0

            metrics_output += (
                f'price_diesel{{fuel="diesel",name="{station_name}"}} '
                f'{data["station"]["diesel"]}\n'
            )
            metrics_output += (
                f'price_e5{{fuel="super-e5",name="{station_name}"}} '
                f'{data["station"]["e5"]}\n'
            )
            metrics_output += (
                f'price_e10{{fuel="super-e10",name="{station_name}"}} '
                f'{data["station"]["e10"]}\n'
            )
            metrics_output += (
                f'open{{name="{station_name}"}} {is_open}\n'
            )

        return Response(metrics_output, mimetype="text/plain; charset=utf-8")
