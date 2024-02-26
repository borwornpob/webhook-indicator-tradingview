# Webhook to indicator (TradingView --> MT5)

# Webhook to Indicator

This project is a simple server that listens for webhook calls from TradingView and performs actions based on the alerts received.

## How to Use

### TradingView Part

1. Set an alert with a webhook calling to the server URL.
2. Format the alert message using this format: `{"Symbol": {{ticker}}, "Direction": "Buy"}`

### Server Part

1. Build the Docker image with `docker build .`
2. Run the Docker container and expose port 8000 with `docker run -p 8000:8000 <image_id>`
3. Visit `<server_url>/docs` to read the API documentation (the server uses FastAPI).

## Documentation

The server API documentation is available at `<server_url>/docs`. It provides detailed information about the available endpoints, their parameters, and responses.


## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file for the full license text.