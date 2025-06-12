"""Tests for `monggregate.operators.accumulators` subpackage."""

from monggregate.operators.accumulators.accumulator import Accumulator, AccumulatorEnum
from monggregate.operators.accumulators.avg import Average, avg
from monggregate.operators.accumulators.count import Count, count
from monggregate.operators.accumulators.first import First, first
from monggregate.operators.accumulators.last import Last, last
from monggregate.operators.accumulators.max import Max, max
from monggregate.operators.accumulators.min import Min, min
from monggregate.operators.accumulators.push import Push, push
from monggregate.operators.accumulators.sum import Sum, sum