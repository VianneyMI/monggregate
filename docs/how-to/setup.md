This guide will show you how to setup an Atlas Cluster and download sample data to follow the tutorial and play with monggregate.

## **Instructions**

**1.** The first step is to **create an Atlas account** (if you do not have one already). You can do it [here](https://www.mongodb.com/cloud/atlas/register).<br>
Simply fill the form and click on "Create your Atlas account". You can even sign up with Google.

**2.** Once your account is created, you will to **create a free tier cluster**. Click on "Build a Database" and follow the steps.<br>
Select the M0 free cluster.<br> 
You can choose the cloud provider and the region that yout want.
Name your cluster as pleased and click on "Create Cluster". 

**3.** Once your cluster is created, you will need to **create a database user** and **whitelist your ip**.<br>
You should be redirected to a security quickstart page guiding you to create a database user and adding your IP address to the IP access whitelist.<br>

**4.** Click on the three dots next to Browse Collections and then on "Load Sample Dataset".<br>
This might take a few minutes.

**5.** You are now ready to follow the tutorial. You can find the first page [here](getting-started.md).
You should now see the following databases when clicking on "Browse Collections".

* `sample_airbnb`
* `sample_analytics`
* `sample_geospatial`
* `sample_guides`
* `sample_mflix`
* `sample_restaurants`
* `sample_supplies`
* `sample_training`
* `sample_weatherdata`

## **References**

* [This video](https://www.youtube.com/watch?v=rPqRyYJmx2g&t=278s) shows the above steps.
* [This guide]() briefly encompasses the above steps and goes a step further by showing you how to connect to your database in python with pymongo.

