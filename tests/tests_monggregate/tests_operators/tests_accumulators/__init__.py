"""Tests for `monggregate.operators.accumulators` subpackage."""

from tests.tests_monggregate.tests_operators.tests_accumulators.test_accumulator import Accumulator, AccumulatorEnum
from tests.tests_monggregate.tests_operators.tests_accumulators.test_avg import Average, avg
from tests.tests_monggregate.tests_operators.tests_accumulators.test_count import Count, count
from tests.tests_monggregate.tests_operators.tests_accumulators.test_first import First, first
from tests.tests_monggregate.tests_operators.tests_accumulators.test_last import Last, last
from tests.tests_monggregate.tests_operators.tests_accumulators.test_max import Max, max
from tests.tests_monggregate.tests_operators.tests_accumulators.test_min import Min, min
from tests.tests_monggregate.tests_operators.tests_accumulators.test_push import Push, push
from tests.tests_monggregate.tests_operators.tests_accumulators.test_sum import Sum, sum