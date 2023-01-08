"""
Expressions Sub-package

MongoDB Online Documentation

Expressions
---------------------

Expressions can include field paths, literals, system variables, expression objects, and
expression operators. Expressions can be nested.

Field Paths
--------------------
Aggregation expressions use field path to access fields in the input documents.
To specify a field path, prefix the field name or the dotted field name (if the field is in the embedded document) with a dollar sign $.
For example, "$user" to specify the field path for the user field or "$user.name" to specify the field path to "user.name" field.

"$<field>" is equivalent to "$$CURRENT.<field>" where the
CURRENT is a system variable that defaults to the root of the current object, unless stated otherwise in specific stages.

Aggregation Variables
---------------------
MongoDB provides various aggregation system variables for use in expressions. To access variables, prefix the variable name with $$. For example:

For a more detailed description of these variables, see system variables.

Literals
-------------------
Literals can be of any type. However, MongoDB parses string literals that start with a dollar sign $ as a path to a field and numeric/boolean literals
in expression objects as projection flags. To avoid parsing literals, use the
$literal expression.

Expression Objects
-------------------

Expression objects have the following form:

   >>> { <field1>: <expression1>, ... }

If the expressions are numeric or boolean literals, MongoDB treats the literals as projection flags (e.g. 1 or true to include the field),
valid only in the $project stage. To avoid treating numeric or boolean literals as projection flags, use the
$literal expression to wrap the numeric or boolean literals.

Operator Expressions
-----------------------

Operator expressions are similar to functions that take arguments.
In general, these expressions take an array of arguments and have the following form:

    >>> { <operator>: [ <argument1>, <argument2> ... ] }

If operator accepts a single argument, you can omit the outer array designating the argument list:

    >>> { <operator>: <argument> }

To avoid parsing ambiguity if the argument is a literal array,
you must wrap the literal array in a $literal expression or keep the outer array that designates the argument list.

Arithmetic Expression Operators
-------------------------------

Arithmetic expressions perform mathematic operations on numbers. Some arithmetic expressions can also support date arithmetic.

See operators sub-package

Array Expression Operators
------------------------------
See operators sub-package

Boolean Expression Operators
------------------------------

Boolean expressions evaluate their argument expressions as booleans and return a boolean as the result.
In addition to the false boolean value, Boolean expression evaluates as false the following: null, 0, and undefined values. T
he Boolean expression evaluates all other values as true, including non-zero numeric values and arrays.

See operators sub-package

Comparison Expression Operators
-------------------------------
Comparison expressions return a boolean excep for $cmp which returns a number.

The comparison expressions take two argument expressions and compare both value and type,
using the specified BSON comparison order for values of different types.


"""
