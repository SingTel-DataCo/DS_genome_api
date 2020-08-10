# Mobility Genome API
This is a python package for Dspark API. It includes api requests for discrete visit, stay point, link meta, od matrix and od through link.

# Dependency
Python 3.*

# API version
discrete visit: v2

stay point: v2

od matrix: v3

od through link: v1

link meta: v1

# API Basic Element:
please refer to https://dataspark.atlassian.net/wiki/spaces/Peking/pages/777847016/Common+API+Elements

# Install
please pull the repo by running following command:

```bash
git pull https://github.com/Jingxuan-Wang/DS_genome_api.git
```

check into the package folder and run:

```bash
python3 setup.py build

python3 setup.py install
```

or using whl file to install:

```bash
pip install *.whl
```

# Usage

## Latest Change

### URL parameter
```python
from genomeapi.dspark import Dspark

url = 'https://staging-presto.dsparkanalytics.com.au'
dspark = Dspark(URL = url)

## Default URL: 'https://apistore.dsparkanalytics.com.au'
dspark = Dspark()
```

### For Extraction Fn
```python
from genomeapi.elements import ExtractionFn
## string extraction function example
string_extraction_fn = ExtractionFn(typ='substring') # not 'string' as type
string_extraction_fn(index=1, length=4)

## time format extraction function example

time_format_extraction_fn = ExtractionFn(typ='timeFormat') # not 'time' as type
time_format_extraction_fn(format='EEEE', timezone='Australia/Sydney')
```

## Basic Query
```python
from genomeapi.dspark import Dspark

## proxies(optional)
proxies = {'http': 'http://10.10.1.10:3128', 'https': 'http://10.10.1.10:1080',}
## with proxies
dspark = Dspark(proxies=proxies)

## without proxies
dspark = Dspark()

dspark.stay_point.dates(begin_date="2019-06-15")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period="PT1H")
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique")

## posting request to api and get data
data = dspark.stay_point.request()

## converting data into a pandas DataFrame
dspark.stay_point.to_df(data)

## getting query in json format
dspark.stay_point.json
```

## Switch endpoint
```python
dspark.stay_point ## endpoint for stay point v2
dspark.od_matrix ## endpoint for od matrix v3
dspark.discrete_vist ## endpoint for discrete visit v2
dspark.od_through_link ## endpoint for od through link v1
dspark.link_meta ## endpoint for link meta v1
```

## Multiple aggregations
```python
dspark.od_matrix.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
dspark.od_matrix.aggregate(metric="total_stays", typ="doubleSum", described_as="total_stays")
```

## Stackable Dimension Facets
```python
from genomeapi.elements import DimensionFacet, ExtractionFn
dfacet = DimensionFacet("extraction")
extraction = ExtractionFn("timeFormat")
dfacets = ["origin_sa4","origin_sa3", dfacet(dimension="__time",output_name="hour",extraction_fn=extraction(format="HH",timezone="Australia/Brisbane"))]
dspark.od_matrix.dimension_facets(dfacets)
```

## Filter
```python
from genomeapi.elements import Filter
filter = Filter()
## normal filter example
dspark.stay_point.filter(filter.in_filter("VIC17483860", "VIC6052402","NSW500187142", dimension="link_id"))

## logic filter exmaple AND
filter = Filter()
and_filter = filter.selector(dimension='agent_gender', value='M') \
    & filter.selector(dimension='agent_home_state', value='1')
dspark.stay_point.filter(and_filter)

## logic filter exmaple OR
filter = Filter()
or_filter = filter.selector(dimension='agent_gender', value='M') \
    | filter.selector(dimension='agent_home_state', value='1')
dspark.stay_point.filter(or_filter)

## logic filter exmaple NOT
filter = Filter()
not_filter = ~filter.selector(dimension='agent_gender', value='M')
dspark.stay_point.filter(not_filter)
```

## Clear out previous query
```python
dspark.stay_point.clear_all()
```

# Authorize
Method 1:
Please put your key and secret into config/genome_api.ini in root directory. Example for genome_api.ini would be:

```
[DEFAULT]
consumer_key = *****************
consumer_secret = ***************
```

Method 2:
set 'consumer_key' and 'consumer_secret' as environment variable

```python
## setting envior in jupyter
%env consumer_key = *********
%env consumer_secret = *********
``` 

Method 3:
provide 'token' as a string variable
```python
token = *********
from genomeapi.dspark import Dspark
dspark = Dspark(token=token)
```

# Development Log
## 1.0.8
1. Workaround for API limitation of multiple extraction functions on same dimension
2. Fix a issue that cause or operation not working for a list of and filter and vice versa 

## 1.0.7
1. Allow multiple extraction dimensions as both list or multiple unnamed parameters

## 1.0.6
1. Make LinkMeta API functional
2. Make dimension facets stackable.

## 1.0.5
1. Add proxies(optional) for api request

## 1.0.4
1. fix the issue that filter doesn't allow multiple layers of logical operations

## 1.0.3
1. change response error from RequestException to ResponseException in order to show more detailed error return from API
2. Add RequestException message when api return is empty

