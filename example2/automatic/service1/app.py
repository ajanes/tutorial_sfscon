import os

import requests
from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

SERVICE2_URL = os.environ.get("SERVICE2_URL", "http://service2:5000/")

app = Flask(__name__)

_tracing_configured = False

if not _tracing_configured:
    resource = Resource.create({"service.name": "service1"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.environ.get("JAEGER_AGENT_HOST", "jaeger"),
        agent_port=int(os.environ.get("JAEGER_AGENT_PORT", "6831")),
    )
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
    _tracing_configured = True


@app.get("/")
def index():
    """Fetch a response from service2 and wrap it with service1 metadata."""
    upstream = requests.get(SERVICE2_URL, timeout=5)
    upstream.raise_for_status()
    return jsonify(service="service1", upstream=upstream.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
