"""Constants and types definitions related to expressions"""

# 3rd Party imports
# ---------------------------
from pydantic import ConstrainedStr

# Package imports
# ---------------------------
from monggregate.index import AggregationVariableEnum

# Constants (Aggregation Variables)
#-------------------------------------------
CLUSTER_TIME = AggregationVariableEnum.CLUSTER_TIME.value
NOW = AggregationVariableEnum.NOW.value
ROOT = AggregationVariableEnum.ROOT.value
CURRENT = AggregationVariableEnum.CURRENT.value
REMOVE = AggregationVariableEnum.REMOVE.value
DESCEND = AggregationVariableEnum.DESCEND.value
PRUNE = AggregationVariableEnum.PRUNE.value
KEEP = AggregationVariableEnum.KEEP.value
