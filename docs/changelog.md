# Monggregate Changelog

All notable changes to this project will be documented in this file.

---

## 🚀 [0.21.0](https://github.com/monggregate/monggregate/releases/tag/v0.21.0) - 2024-04-17
<details>
<summary>Details</summary>
<br>
Identical to 0.21.0b1.
</details>

## 🧪 [0.21.0b1](https://github.com/monggregate/monggregate/releases/tag/v0.21.0b1) - 2024-04-17
<details>
<summary>Details</summary>
<br>
<h3>📖 Documentation</h3>
<p>Improved docstrings in stages and operators.</p>
</details>

## 🧪 [0.21.0b0](https://github.com/monggregate/monggregate/releases/tag/v0.21.0b0) - 2024-01-30
<details>
<summary>Details</summary>
<br>
<h3>✨ New Features</h3>
<p>Implemented <code>VectorSearch</code> pipeline stage.</p>
</details>

---

## 🚀 [0.20.0](https://github.com/monggregate/monggregate/releases/tag/v0.20.0) - 2024-01-27
<details>
<summary>Details</summary>
<br>
<h3>🐛 Bug Fixes</h3>
<p>Fixed bug in <code>Search</code> where some arguments were not properly forwarded to the appropriate operators.</p>

<h3>📖 Documentation</h3>
<p>Added documentation for <code>search</code> and <code>search_meta</code> pipeline stages.</p>
</details>

---

## 🚀 [0.19.1](https://github.com/monggregate/monggregate/releases/tag/v0.19.1) - 2023-12-28
<details>
<summary>Details</summary>
<br>
<h3>🐛 Bug Fixes</h3>
<p>Fixed build, packaging and release process.</p>
</details>

---

## 🚀 [0.19.0](https://github.com/monggregate/monggregate/releases/tag/v0.19.0) - 2023-12-20
<details>
<summary>Details</summary>
<br>
Failed attempt to fix previously broken release.
</details>

---

## 🚀 [0.18.0](https://github.com/monggregate/monggregate/releases/tag/v0.18.0) - 2023-11-12
<details>
<summary>Details</summary>
<br>
<blockquote>⚠️ This release is not available on PyPI as it was broken.</blockquote>

<h3>🐛 Bug Fixes</h3>
<p>Fixed bug preventing use of <code>Compound</code> operator with <code>Search</code> and <code>SearchMeta</code> classes.</p>

<h3>✨ New Features</h3>
<ul>
  <li>Pipelinized <code>Search</code> and <code>SearchMeta</code> classes. Complex expressions can now be built step by step by chaining operators.</li>
  <li>Updated <code>search</code> method in <code>Pipeline</code> class to ease the use of search stages.</li>
  <li>Clarified and simplified faceted search.</li>
</ul>

<h3>♻️ Refactoring</h3>
<ul>
  <li>Use operators rather than statement in <code>Compound</code> class.</li>
  <li>Factorized <code>Search</code> and <code>SearchMeta</code> classes by creating a <code>SearchBase</code> class.</li>
  <li>Use <code>CountOptions</code> rather than raw dicts.</li>
  <li>Created <code>AnyStage</code> union type.</li>
</ul>

<h3>📖 Documentation</h3>
<p>Spelling and grammar fixes.</p>
</details>

---

## 🚀 [0.17.0](https://github.com/monggregate/monggregate/releases/tag/v0.17.0) - 2023-10-26
<details>
<summary>Details</summary>
<br>
<h3>📖 Documentation</h3>
<p>First version of the documentation 🍾!</p>
</details>

---

## 🚀 [0.16.2](https://github.com/monggregate/monggregate/releases/tag/v0.16.2) - 2023-09-17
<details>
<summary>Details</summary>
<br>
<h3>🐛 Bug Fixes</h3>
<p>Allow use of iterables and dicts to group by in <code>Group</code> class and pipeline group function.</p>
</details>

---

## 🚀 [0.16.1](https://github.com/monggregate/monggregate/releases/tag/v0.16.1) - 2023-09-08
<details>
<summary>Details</summary>
<br>
<h3>🐛 Bug Fixes</h3>
<p>Fixed <code>replace_root</code> by passing document argument to <code>ReplaceRoot</code> class.</p>
</details>

---

## 🚀 [0.16.0](https://github.com/monggregate/monggregate/releases/tag/v0.16.0) - 2023-08-29
<details>
<summary>Details</summary>
<br>
<h3>✨ New Features</h3>
<ul>
  <li>Created <code>S</code> object (represents <code>$</code> sign since it is not a valid variable name in Python) to store all MongoDB operators and to create references to fields.</li>
  <li>Created <code>SS</code> object (represents <code>$$</code>) to store aggregation variables and references to user variables.</li>
  <li>Interfaced new operators: <code>add</code>, <code>divide</code>, <code>multiply</code>, <code>pow</code>, <code>subtract</code>, <code>cond</code>, <code>if_null</code>, <code>switch</code>, <code>millisecond</code>, <code>date_from_string</code>, <code>date_to_string</code>, <code>type_</code>.</li>
  <li>Integrated new operators in <code>Expressions</code> class.</li>
</ul>

<h3>♻️ Refactoring</h3>
<ul>
  <li>Redefined <code>Expressions</code> completely. Simplified and clarified how they can be used.</li>
  <li>Removed index module from the root of the package (<code>monggregate.index.py</code> → ∅).</li>
  <li>Removed expressions subpackage (<code>monggregate.expression</code> → ∅).</li>
  <li>Moved expressions fields module to the root (<code>monggregate.expressions.fields.py</code> → <code>monggregate.fields.py</code>).</li>
  <li>Removed expressions aggregation_variables module (<code>monggregate.expression.aggregation_variables.py</code> → ∅).</li>
  <li>Moved enums to more relevant locations (e.g., <code>OperatorEnum</code> is now in <code>monggregate.operators.py</code>).</li>
</ul>

<h3>💥 Breaking Changes</h3>
<ul>
  <li>Operators now return Python objects rather than expressions/statements.</li>
  <blockquote><strong>Note</strong>: The wording might change for clarification purposes.
  "statement" might be renamed "expression" and "resolve" might be renamed "express".
  Some argument names in operators might need to be renamed.</blockquote>
  <li>Expressions subpackage has been restructured with some parts being removed.</li>
</ul>

<h3>📖 Documentation</h3>
<p>Updated README to reflect changes in the package, focusing on the recommended usage and clarifying MongoDB operators.</p>
</details>

---

## 🚀 [0.15.0](https://github.com/monggregate/monggregate/releases/tag/v0.15.0) - 2023-08-09
<details>
<summary>Details</summary>
<br>
<h3>🐛 Bug Fixes</h3>
<ul>
  <li>Fixed bug in <code>Search.from_operator()</code> classmethod due to recent change in operator type in <code>Search</code> class.</li>
  <li>Fixed misspelled operators in constructors map in <code>Search</code> class.</li>
  <li>Fixed missing aliases and missing kwargs reduction in some <code>Search</code> operators.</li>
</ul>
</details>

---

## 🚀 [0.14.1](https://github.com/monggregate/monggregate/releases/tag/v0.14.1) - 2023-08-06
<details>
<summary>Details</summary>
<br>
<h3>🐛 Bug Fixes</h3>
<p>Fixed autocompletion.</p>

<h3>♻️ Refactoring</h3>
<p>Import pydantic into <code>base.py</code> and use <code>base.py</code> to access pydantic features.</p>
</details>

---

## 🚀 [0.14.0](https://github.com/monggregate/monggregate/releases/tag/v0.14.0) - 2023-07-23
<details>
<summary>Details</summary>
<br>
<h3>⬆️ Upgrades</h3>
<p>Made package compatible with Pydantic V2.</p>

<h3>♻️ Refactoring</h3>
<ul>
  <li>Used an import trick to still use Pydantic V1 even in environments using Pydantic V2.</li>
  <li>Centralized pydantic import into <code>base.py</code> to avoid having to use import trick in multiple files.</li>
</ul>

<h3>📖 Documentation</h3>
<ul>
  <li>Updated README to better reflect current state of the package.</li>
  <li>Started a changelog! 🍾</li>
  <li>Major improvements to documentation.</li>
</ul>
</details>


## What about previous versions?

Prior to 0.14.0, the changelog was not kept.
