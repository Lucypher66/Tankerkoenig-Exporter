
# Tankerkoenig Exporter

A Prometheus exporter for Tankerkoenig fuel price data.

## Preparation

Before starting, ensure you have:
- Python 3.8 or higher
- pip package manager
- systemd (for service management)
- Prometheus instance running

## Obtaining your API key
You can get your API key by registerering at the following link:
https://onboarding.tankerkoenig.de/

## Obtaining GUIDs of target gas stations
You can find the GUIDs of your favored gas stations here:
https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html

You can configure up to 10 gas stations inside the configuration file.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Lucypher66/Tankerkoenig-Exporter.git
cd Tankerkoenig-Exporter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the exporter:
```bash
cp config.example.yml config.yml
# Edit config.yml with your settings
```

## You can turn any page on or off. The index page is empty. 

## Caution!
The config page displays your current config in the browser. This is for diagnostic purposes only. It is exposing your API Key in the browser. 

## Systemd Service File
### Create a user for the gas price exporter to run as (e.g. gas-exporter). Alternatively you can use a present user.


```
[Unit]
Description=Gas prices exporter for prometheus using the tankerkoenig API
After=network.target
Wants=network-online.target

[Service]
Restart=always
Type=simple
ExecStart=python3 -m gunicorn main:app -b 0.0.0.0:8000
WorkingDirectory=/home/gas-exporter
User=gas-exporter

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable tankerkoenig-exporter
sudo systemctl start tankerkoenig-exporter
```

## Prometheus Configuration

### Make sure Prometheus is not requesting too frequent or else you may be subjected to a rate limit.

Add to your `prometheus.yml`:

```yaml
scrape_configs:
    - job_name: 'tankerkoenig'
        static_configs:
            - targets: ['localhost:8000']
        scrape_interval: 5m
        scrape_timeout: 10s
```

Reload Prometheus to apply changes.
