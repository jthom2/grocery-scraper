# custom assertions for performance regression testing
from typing import Optional, Union


# subclass allows catching performance errors separately
class PerformanceAssertionError(AssertionError):
    pass


# fails if latency exceeds threshold + tolerance buffer
def assert_latency_under(
    actual_ms: float,
    threshold_ms: float,
    tolerance_pct: float = 10,
    message: Optional[str] = None,
) -> None:
    allowed_ms = threshold_ms * (1 + tolerance_pct / 100)

    if actual_ms > allowed_ms:
        if message is None:
            message = (
                f"Latency regression detected:\n"
                f"  Actual: {actual_ms:.2f}ms\n"
                f"  Threshold: {threshold_ms:.2f}ms\n"
                f"  Tolerance: {tolerance_pct}% ({threshold_ms * tolerance_pct / 100:.2f}ms)\n"
                f"  Allowed: {allowed_ms:.2f}ms"
            )
        raise PerformanceAssertionError(message)


# validates optimization work actually reduced latency
def assert_latency_improved(
    actual_ms: float,
    baseline_ms: float,
    min_improvement_pct: float = 5,
    message: Optional[str] = None,
) -> None:
    improvement_pct = ((baseline_ms - actual_ms) / baseline_ms) * 100

    if improvement_pct < min_improvement_pct:
        if message is None:
            message = (
                f"Expected performance improvement not achieved:\n"
                f"  Baseline: {baseline_ms:.2f}ms\n"
                f"  Actual: {actual_ms:.2f}ms\n"
                f"  Improvement: {improvement_pct:.2f}%\n"
                f"  Required: {min_improvement_pct:.2f}%"
            )
        raise PerformanceAssertionError(message)


# detects flaky performance via coefficient of variation
def assert_latency_consistent(
    measurements: list[float],
    variance_pct: float = 20,
    message: Optional[str] = None,
) -> None:
    if len(measurements) < 2:
        raise ValueError("Need at least 2 measurements for consistency check")

    mean = sum(measurements) / len(measurements)
    variance = sum((x - mean) ** 2 for x in measurements) / len(measurements)
    std_dev = variance ** 0.5
    coefficient_of_variation = (std_dev / mean) * 100

    if coefficient_of_variation > variance_pct:
        if message is None:
            message = (
                f"Performance variance exceeds threshold:\n"
                f"  Mean: {mean:.2f}ms\n"
                f"  Std Dev: {std_dev:.2f}ms\n"
                f"  Coefficient of Variation: {coefficient_of_variation:.2f}%\n"
                f"  Allowed: {variance_pct:.2f}%"
            )
        raise PerformanceAssertionError(message)


# validates caching is actually reducing redundant requests
def assert_cache_hit_rate(
    hit_rate: float,
    expected_rate_pct: float,
    tolerance_pct: float = 5,
    min_requests: int = 10,
    actual_requests: Optional[int] = None,
    message: Optional[str] = None,
) -> None:
    if actual_requests is not None and actual_requests < min_requests:
        raise ValueError(
            f"Insufficient requests ({actual_requests}) for reliable cache "
            f"assertion (minimum: {min_requests})"
        )

    lower_bound = expected_rate_pct - tolerance_pct
    upper_bound = expected_rate_pct + tolerance_pct

    if not (lower_bound <= hit_rate <= upper_bound):
        if message is None:
            message = (
                f"Cache hit rate regression detected:\n"
                f"  Actual: {hit_rate:.2f}%\n"
                f"  Expected: {expected_rate_pct:.2f}%\n"
                f"  Tolerance: ±{tolerance_pct:.2f}%\n"
                f"  Valid Range: [{lower_bound:.2f}%, {upper_bound:.2f}%]"
            )
        raise PerformanceAssertionError(message)


# catches request bloat that increases latency
def assert_request_count_under(
    actual_requests: int,
    max_requests: int,
    message: Optional[str] = None,
) -> None:
    if actual_requests > max_requests:
        if message is None:
            message = (
                f"Request count regression detected:\n"
                f"  Actual: {actual_requests}\n"
                f"  Maximum: {max_requests}"
            )
        raise PerformanceAssertionError(message)


# validates system can handle required load
def assert_throughput(
    total_operations: int,
    duration_seconds: float,
    min_ops_per_second: float,
    message: Optional[str] = None,
) -> None:
    actual_throughput = total_operations / duration_seconds if duration_seconds > 0 else 0

    if actual_throughput < min_ops_per_second:
        if message is None:
            message = (
                f"Throughput regression detected:\n"
                f"  Actual: {actual_throughput:.2f} ops/sec\n"
                f"  Minimum: {min_ops_per_second:.2f} ops/sec"
            )
        raise PerformanceAssertionError(message)


# fails ci if latency increased too much vs baseline
def assert_no_regression(
    actual_ms: float,
    baseline_ms: float,
    regression_threshold_pct: float = 20,
    message: Optional[str] = None,
) -> None:
    if baseline_ms <= 0:
        raise ValueError("Baseline must be positive")

    regression_pct = ((actual_ms - baseline_ms) / baseline_ms) * 100

    if regression_pct > regression_threshold_pct:
        if message is None:
            message = (
                f"Performance regression detected:\n"
                f"  Baseline: {baseline_ms:.2f}ms\n"
                f"  Actual: {actual_ms:.2f}ms\n"
                f"  Regression: {regression_pct:.2f}%\n"
                f"  Threshold: {regression_threshold_pct:.2f}%"
            )
        raise PerformanceAssertionError(message)
