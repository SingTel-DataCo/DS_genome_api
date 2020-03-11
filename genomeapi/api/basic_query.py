__author__ = 'jingxuan'
from genomeapi.elements import Dates, Aggregation, DimensionFacet, LogicFilter, RequestException
from genomeapi.elements import Granularity, Location, TimeSeriesReference

import json
import requests
from requests.status_codes import codes
from pandas import json_normalize

class BasicQuery:
  _URLS = "https://apistore.dsparkanalytics.com.au"
  _API_ENDPOINT = {"discretevisit": "v2",
                   "staypoint": "v2",
                   "odmatrix": "v3",
                   "odthroughlink": "v1",
                   "linkmeta": "v1"}
  def __init__(self, end_point:str, token:str = ""):
    self.query_path = "/".join([self._URLS, end_point, self._API_ENDPOINT[end_point], 'query'])
    self.token = token
    self._dt = None
    self._aggs = None
    self._ts_reference = None
    self._d_facets = None
    self._grant = None
    self._loc = None
    self._filt = None
    self.req = {}

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

  def dimension_facets(self, *dimension, output_name=None, typ="String"):
    d_facets = DimensionFacet()
    self._d_facets = d_facets(*dimension, output_name=output_name, typ=typ)
    return self

  def granularity(self, period, typ="period"):
    grant = Granularity()
    self._grant = grant(period, typ)
    return self

  def location(self, location_type, level_type, id, country="AU"):
    loc = Location(country=country)
    self._loc = loc(location_type, level_type, id)
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
    self.req.update(self._dt)
    self.req.update(self._aggs.to_dict())
    self.req.update(self._grant)

    if self._loc is not None:
      self.req.update(self._loc)

    if self._ts_reference is not None:
      self.req.update(self._ts_reference)

    if self._filt is not None:
      self.req.update(self._filt)

    if self._d_facets is not None:
      self.req.update(self._d_facets)

    self.json = json.dumps(self.req)
    
  def request(self):
    if len(self.req) == 0:
      self.dumps()
    response = requests.post(self.query_path,
                            data=self.json,
                            headers={
                             'Authorization': 'Bearer '+ self.token,
                              'Content-Type': 'application/json'
                            })

    if response.status_code != codes['ok']:
      raise RequestException(response)
    else:
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
    self.req = {}
    return self