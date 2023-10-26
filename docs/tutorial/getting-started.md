## **Installing monggregate**

`monggregate` is available on PyPI:

```shell
pip install monggregate
```
## **Requirements**

It requires python > 3.10 and has a few required dependencies such as `pydantic`, `pyhumps` and `typing-extensions`.

If it as a good query builder it helps you build the query, in order to execute them you will need a MongoDB driver.

For more details about the requirements, see the requirements files [in the repo](https://github.com/VianneyMI/monggregate/blob/main/requirements). 

## **First steps**

There are several ways you may use monggregate.

You can use the stages individually and build your pipeline step by step or you can use the `Pipeline` class to build your pipeline. That's actually the way I recommend you to use it.

In that cases, your first steps will look like this:

```python

from monggregate import Pipeline

pipeline = Pipeline()
```

Now when writing,

```python

pipeline.
```

your IDE will show you the available stages.

You should see something like this.

![autocompletion](../img/demo_autocompletion.png)

In the [next page](pipeline.md), we will see in more details how to use the `Pipeline` class.