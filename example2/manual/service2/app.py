import os

from flask import Flask, jsonify, request
from opentelemetry import propagate, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = Flask(__name__)

_tracing_configured = False

if not _tracing_configured:
    resource = Resource.create({"service.name": "service2"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.environ.get("JAEGER_AGENT_HOST", "jaeger"),
        agent_port=int(os.environ.get("JAEGER_AGENT_PORT", "6831")),
    )
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    _tracing_configured = True

tracer = trace.get_tracer("service2")


@app.get("/")
def index():
    """Return a simple payload consumed by service1."""
    context = propagate.extract(request.headers)
    with tracer.start_as_current_span("service2.index", context=context):
        return jsonify(service="service2", message="Hello from service2")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
