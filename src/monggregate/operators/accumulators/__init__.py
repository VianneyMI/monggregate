"""Accumulator Operators Subpackage"""

from monggregate.operators.accumulators.avg import Average, Avg, average, avg
from monggregate.operators.accumulators.count import Count, count
from monggregate.operators.accumulators.first import First, first
from monggregate.operators.accumulators.last import Last, last
from monggregate.operators.accumulators.min import Min, min
from monggregate.operators.accumulators.max import Max, max
from monggregate.operators.accumulators.push import Push, push
from monggregate.operators.accumulators.sum import Sum, sum

# TODO  :
# * $accumulator
# * $addToSet
# * $bottom
# * $bottomN
# * $firstN
# * $lastN
# * $maxN
# * $mergeObjects
# * $stdDedPop
# * $stdDevSamp
# * $top
# * $topN
