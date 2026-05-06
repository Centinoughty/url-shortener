# URL Shortener

A URL shortener is a service that takes a long URL and generates a shorter, unique alias that redrects to the original URL.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+ (for local development)


## Installation

Create `.env` based on the `.env.example` for running the application.

You need to install `docker` on your system to run this app.

```bash
docker compose up -d --build
```

To see the logs of the application:

```bash
docker compose logs -f app
```


## Usage

### Shorten a URL

```bash
curl -X POST "http://localhost:5000/shorten?long_url=https://example.com/very/long/url"
```

Response:
```json
{
  "short_url": "abc123"
}
```

### Redirect to original URL

```bash
curl http://localhost:5000/abc123
```

This redirects to the original long URL.
