#  Copyright © DataSpark Pte Ltd 2014 - 2020.
#
#  This software and any related documentation contain confidential and proprietary information of
#  DataSpark and its licensors (if any). Use of this software and any related documentation is
#  governed by the terms of your written agreement with DataSpark. You may not use, download or
#  install this software or any related documentation without obtaining an appropriate licence
#  agreement from DataSpark.
#
#  All rights reserved.

"""
   This is basic operations for API query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

import json
import requests
from requests.status_codes import codes
try:
  from pandas import json_normalize
except:
  from pandas.io.json import json_normalize

from genomeapi.elements import element
from genomeapi.elements import Dates, Aggregation, DimensionFacet, LogicFilter, ResponseException, RequestException
from genomeapi.elements import Granularity, Location, TimeSeriesReference
from genomeapi.elements.element import Element

class BasicQuery:
  _URLS = "https://apistore.dsparkanalytics.com.au"
  _API_ENDPOINT = {"discretevisit": "v2",
                   "staypoint": "v2",
                   "odmatrix": "v3",
                   "odthroughlink": "v1",
                   "linkmeta": "v1"}
  def __init__(self, end_point:str, token:str = "", proxies: dict = {}):
    self._query_path = "/".join([self._URLS, end_point, self._API_ENDPOINT[end_point], 'query'])
    self._token = token
    self._dt = None
    self._aggs = None
    self._ts_reference = None
    self._d_facets = None
    self._grant = None
    self._loc = None
    self._filt = None
    self._req = {}
    self._proxies = proxies

  def dates(self, begin_date: str, end_date: str = None):
    dt = Dates()
    self._dt = dt(begin_date, end_date=end_date)
    return self

  def aggregate(self, metric: str, typ: str, described_as=None):
    agg = Aggregation()
    if self._aggs is None:
      self._aggs = agg(metric=metric, typ=typ, described_as=described_as) ## assign self.aggs as Aggregations Object
    else:
      self._aggs += agg(metric=metric, typ=typ, described_as=described_as) ## adding other Aggregations Object to self.aggs
    return self

  def checkdimfacettyp(self, value):
    if isinstance(value, str):
      dfacet = DimensionFacet(typ="string")
      return dfacet(dimension=value)
    else:
      return value

  def dimension_facets(self, dimension=None, output_name=None, value=None, extraction_fn=None, typ="string"):
    d_f = DimensionFacet(typ=typ)
    self._d_facets = d_f(dimension=dimension, value=value, output_name=output_name, extraction_fn=extraction_fn).to_dict()
    return self

  def granularity(self, period, typ="period"):
    grant = Granularity()
    self._grant = grant(period, typ)
    return self

  def location(self, location_type, level_type, id, country="AU", direction=None):
    loc = Location(country=country)
    self._loc = loc(location_type, level_type, id, direction)
    return self

  def filter(self, filt):
    if isinstance(filt, LogicFilter):
      self._filt = filt.to_dict()
    elif isinstance(filt, dict):
      self._filt = filt
    return self

  def time_series_reference(self,v):
    ts = TimeSeriesReference()
    self._ts_reference = ts(v)
    return self

  def dumps(self):
    self._req.update(self._dt)
    self._req.update(self._aggs.to_dict())
    self._req.update(self._grant)

    if self._loc is not None:
      self._req.update(self._loc)

    if self._ts_reference is not None:
      self._req.update(self._ts_reference)

    if self._filt is not None:
      self._req.update(self._filt)

    if self._d_facets is not None:
      self._req.update(self._d_facets)

    self.json = json.dumps(self._req)
    
  def request(self):
    if len(self._req) == 0:
      self.dumps()

    if len(self._proxies) > 0:
      response = requests.post(self._query_path,
                              data=self.json,
                              headers={
                               'Authorization': 'Bearer ' + self._token,
                                'Content-Type': 'application/json'
                              },
                               proxies=self._proxies)
    else:
      response = requests.post(self._query_path,
                               data=self.json,
                               headers={
                                 'Authorization': 'Bearer ' + self._token,
                                 'Content-Type': 'application/json'
                               })

    if response.status_code != codes['ok']:
      raise ResponseException(response)
    else:
      if len(response.json()) == 0:
        raise RequestException("API return is empty, please check your query, especially the date you are querying")
      return response.json()

  def to_df(self, json_data):
    df = json_normalize(json_data)
    return df

  def clear_all(self):
    self._dt = None
    self._aggs = None
    self._ts_reference = None
    self._d_facets = None
    self._grant = None
    self._loc = None
    self._filt = None
    self._req = {}
    return self
