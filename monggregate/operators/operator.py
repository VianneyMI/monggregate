"""Operator Module"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel, BaseConfig

# Package imports
# ---------------------------
from monggregate.utils import StrEnum

# NOTE : This is the same interface thant the stage class
# => Need a common ancestor
class Operator(BaseModel, ABC):
    """MongoDB operator abstract base class"""

    _statement : dict = {}# TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]

    @property
    @abstractmethod
    def statement(self)->dict:
        """stage stament"""

        # this is a lazy attribute
        # what is currently in generate statement should go in here
        # TODO : Implement cache <VM, 02/10/2022>

    class Config(BaseConfig):
        """Configuration for Stage classes"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True

    def __call__(self)->dict:
        """Makes an instance of stage callable"""

        return self.statement

class OperatorEnum(StrEnum):
    """Enumeration of available operators"""

    # TODO : Check for mispellong <VM, 05/10/2022>
    ABS = "$abs"
    ACCUMULATOR = "$accumulator"
    ACOS = "$acos"
    ACOSH = "$acosh"
    ADD = "$add"
    ADD_TO_SET = "$addToSet"
    ALL_ELEMENTS_TRUE = "$allElementsTrue"
    AND = "$and"
    ANY_ELEMENTS_TRUE = "$anyElementsTrue"
    ARRAY_ELEM_AT = "$arrayElemAt"
    ARRAY_TO_OBJECT = "$arrayToObject"
    ASIN = "$asin"
    ASINH = "$asinh"
    ATAN = "$atan"
    ATAN2 = "$atan2"
    ATANH = "$atanh2"
    AVG = "$avg"
    BINARY_SIZE = "$binarySize"
    BSON_SIZE ="$bsonSize"
    CEIL = "$ceil"
    CMP = "$cmp"
    CONCAT = "$concat"
    CONCAT_ARRAYS = "$concatArrays"
    COND = "$cond"
    CONVERT = "$convert"
    COS = "$cos"
    COSH = "$cosh"
    DATE_FROM_PARTS = "$dateFromParts"
    DATE_FROM_STRING = "$dateFromString"
    DATE_TO_PARTS = "$dateToParts"
    DATE_TO_STRING = "$dateToString"
    DAY_OF_MONTH ="$dayOfMonth"
    DAY_OF_WEEK = "$dayOfWeek"
    DAY_OF_YEAR = "$dayOfYear"
    DEGREES_TO_RADIANS = "$degreesToRadians"
    DIVIDE = "$divide"
    EQ = "$eq"
    EXP = "$exp"
    FILTER = "$filter"
    FIRST = "$first" # two operators one for array one for accumulator
    FLOOR = "$floor"
    FUNCTION = "$function"
    GET_FIELD = "$getField"
    GT = "$gt"
    GTE = "$gte"
    HOUR = "$hour"
    IF_NULL = "$ifNull"
    IN = "$in"
    INDEX_OF_ARRAY = "$indexOfArray"
    INDEX_OF_BYTES = "$indexOfBytes"
    INDEX_OF_CP = "$indexOfCP"
    IS_ARRAY = "$isArray"
    IS_NUMBER = "$isNumber"
    ISO_DAY_OF_WEEK = "$isoDayOfWeek"
    ISO_WEEK = "$isoWeek"
    ISO_WEEK_YEAR ="$isoWeekYear"
    LAST = "$last"
    LET ="$let"
    LITERAL = "$literal"
    LN = "$ln"
    LOG = "$log"
    LOG10 = "$log10"
    LT = "$lt"
    LTE = "$lte"
    LTRIM = "$ltrim"
    MAP = "$map"
    MAX = "$max"
    MERGE_OBJECTS = "$mergeObjects"
    META = "$meta"
    MILLI_SECOND = "$millisecond"
    MIN = "$min"
    MINUTE ="$minute"
    MOD ="$mod"
    MONTH = "$month"
    MULTIPLY ="$multiply"
    NE ="$ne"
    NOT ="$not"
    OBJECT_TO_ARRAY ="$objectToArray"
    OR = "$or"
    POW = "$pow"
    PUSH = "$push"
    RADIANS_TO_DEGREES = "$radiansToDegrees"
    RAND = "$rand"
    RANGE = "$range"
    REDUCE = "$reduce"
    REGEX_FIND ="$regexFind"
    REGEX_FIND_ALL = "$regexFindAll"
    REGEX_MATCH = "$regexMatch"
    REPLACE_ONE ="$replaceOne"
    REPLACE_ALL = "$replaceAll"
    REVERSE_ARRAY = "$reverseArray"
    ROUND = "$round"
    RTRIM = "$rtrim"
    SECOND = "$second"
    SET_DIFFERENCE = "$setDifference"
    SET_EQUALS = "$setEquals"
    SET_FIELD = "$setField"
    SET_INTERSECTION = "$setIntersection"
    SET_IS_SUBSET = "$setIsSubset"
    SET_UNION = "$setUnion"
    SIN = "$sin"
    SINH = "$sinh"
    SIZE ="$size"
    SLICE = "$slice"
    SPLIT = "$split"
    SQRT = "$sqrt"
    STD_DEV_POP = "$stdDevPop"
    STD_DEV_SAMP = "$stdDevSamp"
    STR_LEN_BYTES = "$strLenBytes"
    STR_LEN_CP ="$strLenCP"
    STR_CASE_CMP = "$strcasecmp"
    SUBSTR = "$substr"
    SUBSTR_BYTES = "$substrBytes"
    SUBSTR_CP = "$substrCP"
    SUBSTRACT = "$subtract"
    SUM = "$sum"
    SWITCH = "$switch"
    TAN = "$tan"
    TANH = "$tanh"
    TO_BOOL ="$toBool"
    TO_DATE = "$toDate"
    TO_DECIMAL = "$toDecimal"
    TO_DOUBLE = "$toDouble"
    TO_INT = "$toInt"
    TO_LONG = "$toLong"
    TO_LOWER = "$toLower"
    TO_OBJECT_ID = "$toObjectId"
    TO_STRING = "$toString"
    TO_UPPER = "$toUpper"
    TRIM = "$trim"
    TRUNC = "$trunc"
    TYPE = "$type"
    WEEK = "$week"
    YEAR = "$year"
    ZIP = "$zip"
