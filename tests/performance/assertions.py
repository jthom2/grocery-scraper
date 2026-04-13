"""Performance regression test assertions."""
from typing import Optional, Union


class PerformanceAssertionError(AssertionError):
    """Raised when performance assertion fails."""
    pass


def assert_latency_under(
    actual_ms: float,
    threshold_ms: float,
    tolerance_pct: float = 10,
    message: Optional[str] = None,
) -> None:
    """Assert that latency is under threshold with tolerance.

    Args:
        actual_ms: Actual measured latency in milliseconds
        threshold_ms: Target threshold in milliseconds
        tolerance_pct: Allowed tolerance as percentage of threshold
                      (default 10% = 10ms tolerance on 100ms threshold)
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If actual latency exceeds
                                  threshold + tolerance
    """
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


def assert_latency_improved(
    actual_ms: float,
    baseline_ms: float,
    min_improvement_pct: float = 5,
    message: Optional[str] = None,
) -> None:
    """Assert that latency improved by minimum percentage.

    Args:
        actual_ms: Actual measured latency in milliseconds
        baseline_ms: Baseline latency in milliseconds
        min_improvement_pct: Minimum improvement percentage required
                            (default 5%)
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If improvement is less than minimum
    """
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


def assert_latency_consistent(
    measurements: list[float],
    variance_pct: float = 20,
    message: Optional[str] = None,
) -> None:
    """Assert that latency measurements are consistent.

    Args:
        measurements: List of latency measurements in milliseconds
        variance_pct: Allowed variance as percentage of mean
                     (default 20%)
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If variance exceeds threshold
        ValueError: If fewer than 2 measurements provided
    """
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


def assert_cache_hit_rate(
    hit_rate: float,
    expected_rate_pct: float,
    tolerance_pct: float = 5,
    min_requests: int = 10,
    actual_requests: Optional[int] = None,
    message: Optional[str] = None,
) -> None:
    """Assert that cache hit rate meets expectation.

    Args:
        hit_rate: Actual cache hit rate as percentage (0-100)
        expected_rate_pct: Expected cache hit rate as percentage
        tolerance_pct: Allowed tolerance as percentage (default 5%)
        min_requests: Minimum requests needed for valid assertion
        actual_requests: Actual number of requests made (for validation)
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If hit rate doesn't meet expectation
        ValueError: If insufficient requests for reliable assertion
    """
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


def assert_request_count_under(
    actual_requests: int,
    max_requests: int,
    message: Optional[str] = None,
) -> None:
    """Assert that request count is under maximum.

    Args:
        actual_requests: Actual number of requests made
        max_requests: Maximum allowed requests
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If request count exceeds maximum
    """
    if actual_requests > max_requests:
        if message is None:
            message = (
                f"Request count regression detected:\n"
                f"  Actual: {actual_requests}\n"
                f"  Maximum: {max_requests}"
            )
        raise PerformanceAssertionError(message)


def assert_throughput(
    total_operations: int,
    duration_seconds: float,
    min_ops_per_second: float,
    message: Optional[str] = None,
) -> None:
    """Assert minimum throughput (operations per second).

    Args:
        total_operations: Total operations completed
        duration_seconds: Total duration in seconds
        min_ops_per_second: Minimum required throughput
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If throughput below minimum
    """
    actual_throughput = total_operations / duration_seconds if duration_seconds > 0 else 0

    if actual_throughput < min_ops_per_second:
        if message is None:
            message = (
                f"Throughput regression detected:\n"
                f"  Actual: {actual_throughput:.2f} ops/sec\n"
                f"  Minimum: {min_ops_per_second:.2f} ops/sec"
            )
        raise PerformanceAssertionError(message)


def assert_no_regression(
    actual_ms: float,
    baseline_ms: float,
    regression_threshold_pct: float = 20,
    message: Optional[str] = None,
) -> None:
    """Assert that performance hasn't regressed beyond threshold.

    Args:
        actual_ms: Actual measured latency in milliseconds
        baseline_ms: Baseline latency in milliseconds
        regression_threshold_pct: Allowed regression percentage (default 20%)
        message: Optional custom error message

    Raises:
        PerformanceAssertionError: If regression exceeds threshold
    """
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
