# app/main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from framework.middleware.logging_middleware import LoggingMiddleware
from app.routers.user_info import router as user_info_router

from framework.middleware.correlation_id_middleware import CorrelationIDMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

app = FastAPI()

resource = Resource.create({"service.name": "user-info-service"})
tracer_provider = TracerProvider(resource=resource)
console_exporter = ConsoleSpanExporter()
span_processor = SimpleSpanProcessor(console_exporter)
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)
app.add_middleware(CorrelationIDMiddleware)

app.add_middleware(LoggingMiddleware)
app.add_middleware(OpenTelemetryMiddleware)

app.include_router(user_info_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
