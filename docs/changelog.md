# Release Notes

## 0.18.0

### Fixes

* Fixed bug preventing to use `Compound` operator with `Search` and `SearchMeta` classes.

### New Features

* Pipelinized `Search` and `SearchMeta` classes. That is complex expressions can be built step by step by chaining operators.
* Updated `search` method in `¨Pipeline` class to ease the use of the search stages.
* Clarified and simplified faceted search

### Refactoring

* Use operators rather than statement in `Compound` class
* Factorized `Search` and `SearchMeta` classes by creating a `SearchBase` class
* Use `CountOptions` rather than raw dicts
* Created `AnyStage` union type

### Docs

* Spelling and grammar fixes

## 0.17.0

### Docs

* First version of the documentation :champagne: !

## 0.16.2

### Fixes

* Allow to use iterable and dicts to group by in Group class and pipeline group function

## 0.16.1

### Fixes

* Fixed replace_root by passing document argument to ReplaceRoot class


## 0.16.0

### New Features

* Created S object (represents $ sign since it is not a valid variable name in python) to store all MongoDB operators and to create references to fields
* Created SS object (represents $$) to store aggregation variables and referenes to user variables
* Interfaced a chunk of new operators(add, divide, multiply, pow, substract, cond, if_null, switch, millisecond, date_from_string, date_to_string, type_)
* Integrated new operators in Expressions class


### Refactoring

* Redefined Expressions completely. Simplified and clarified how they can be used when using this package.
* Removed index module that was at the root of the package (monggregate.index.py -> ø) 
* Removed expressions subpackage (monggregate.expression -> ø)
* Moved expressions fields module to the root of the package (monggregate.expressions.fields.py -> monggregate.fields.py)
* Removed expressions aggregation_variables module (monggregate.expression.aggregation_variables.py -> ø)
* Moved the enums that were defined in index to a more relevant place. Ex OperatorEnum is now in monggregate.operators.py

### Breaking Changes

* Operators now return python objects rather than expressions/statements. 
  NOTE: The wording might change for clarification purposes.
        statement might be renamed expression and resolve might renamed express
        To do so, some arguments might need to be renamed in the operators
* Expressions subpackage has been exploded and some parts have been deleted

### Documentation

* Updated readme to reflect changes in the packge. Readme now focuses on the recommended way to use the package and clarifies how to use MongoDB operators.

## 0.15.0

### Fixes

* Fixed bug in `Search.from_operator()` classmethod due to recent change in operator type in `Search` class
* Fixed misspelled operators in constructors map in `Search` class
* Fixed missing aliases and missing kwargs reduction in some `Search` operators


## 0.14.1

### Fixes

* Fixed autocompletion

### Refactoring

* Import pydantic into base.py and using base.py to access pydantic features


## 0.14.0

### Upgrades

* Make package compatible with pydantic V2

### Refactoring

* Use an import trick to still use pydantic V1 even on environments using pydantic V2
* Centralized pydantic import into base.py in order to avoid having to use import trick on multiple files

### Documentation

* Updated readme to better reflect current state of the pacakge.
* Started a changelog ! :champagne:
* Major change in the doc 
