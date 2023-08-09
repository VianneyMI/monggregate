# Release Notes

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
