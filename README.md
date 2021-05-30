# Master Thesis 2021: MySQL Database Integrity Checker
This repository contains the source code for the product associated with the 2021 master thesis project at Roskilde University, written and developed by 

Danny Nielsen & Kim Meyer Albrechtsen.



## Running the Tool

The simplest way to run dIC is to pull the pre-packaged Docker image from Docker Hub and run it in a container:

```bash
$ docker run -it --pull=always --rm dbdness/dic
```

The above command will pull the latest changes to the image, if any, and execute the image in a container with an interactive prompt. When the `root>` prompt is visible, the dIC tool has been initialized succesfully. Run the `help` or `?` commands to get started.

The image comes pre-packaged with the two sample databases described in the last section of this README. To connect to them, run one of the two following commands:

**"Northwind_nofks"**

```bash
db-connect connection-string="host=localhost;database=northwind_nofks;user=demo;password=demo"
```

**"Sakila"**

```bash
db-connect connection-string="host=localhost;database=sakila;user=demo;password=demo"
```



## Sample Data

### Northwind MySQL
The sample data under the *dnikma-thesis-2021/infrastructure/northwind/* folder is from the [dalers/mywind](https://github.com/dalers/mywind) repository, and has been modified slightly for our purposes. The original work is distributed under the BSD 2-Clause "Simplified" License. To view a copy of this license, visit 
https://github.com/dalers/mywind/blob/master/LICENSE.

### MySQL Sakila
The sample data under the *dnikma-thesis-2021/infrastructure/sakila/* folder is from the [datacharmer/test_db](https://github.com/datacharmer/test_db/tree/master/sakila) repository, and has been modified slightly for our purposes. The original work is distributed and licensed under the Creative Commons Attribution-Share Alike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.

