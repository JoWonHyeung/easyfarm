import os
from typing import Callable

from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info, Histogram
from prometheus_client import Counter

NAMESPACE = os.environ.get("METRICS_NAMESPACE", "fastapi")
SUBSYSTEM = os.environ.get("METRICS_SUBSYSTEM", "model")

instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)
## ENABLE_METRICS 가 true 인 Runtime 에서만 동작하게 됨

instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.latency(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)


def model_output(
        metric_name: str = "model_output",
        metric_doc: str = "Output value of cnn model",
        metric_namespace: str = "",
        metric_subsystem: str = "",
) -> Callable[[Info], None]:
    METRIC_Result = Counter(
        "http_user_result_pestName",
        "cnn model output about crop",
        labelnames = ("pestName",)
    )

    METRIC_Input = Counter(
        "http_user_inputPlant",
        "user input Plant",
        labelnames=("inputPlant",)
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/prediction":
            predicted = info.response.headers.get("pestName")
            inputPlant = info.response.headers.get("inputPlant")
            if predicted:
                METRIC_Result.labels(predicted).inc()
                METRIC_Input.labels(inputPlant).inc()

    return instrumentation


instrumentator.add(
    model_output(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM)
)
