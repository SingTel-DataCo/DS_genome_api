__author__ = 'jingxuan'

from .element import Element
from .exceptions import APIException
from .extraction_fn import ExtractionFn

class LogicFilter(Element):
  _ORDER = ['lexicographic', 'alphanumeric', 'numeric', 'strlen']
  _logic = None

  def to_dict(self):
    if self._logic is None:
      return self.form_obj(filter=self.v)
    elif self._logic is 'not':
      v = self.form_obj(field=self.v, type=self._logic)
      return self.form_obj(filter=v)
    else:
      v = self.form_obj(fields=self.v, type=self._logic)
      return self.form_obj(filter=v)

  def selector(self, dimension: str, value:str, extraction_fn=None):
    if extraction_fn is None:
      self.v = self.form_obj(dimension=dimension, value=value, type='selector')
    elif isinstance(extraction_fn, dict):
      if extraction_fn['type'] == "timeFormat" and dimension != "__time":
        raise APIException("Time extraction must use '__time' as dimension")
      self.v = self.form_obj(dimension=dimension, value=value, type='selector', extractionFn=extraction_fn)
    return self

  def in_filter(self, *values, dimension: str):
    self.v = self.form_obj(dimension=dimension, values=list(values), type='in')
    return self

  def bound(self,dimension, lower, ordering, upper=None, **kwargs):
    if upper:
      self.v = self.form_obj(dimension=dimension, lower=int(lower), upper=int(upper), ordering=ordering, type='bound', **kwargs)
      return self
    else:
      self.v = self.form_obj(dimension=dimension, lower=int(lower), ordering=ordering, type='bound', **kwargs)
      return self

  def interval(self,*intervals, dimension: str):
    self.v = self.form_obj(dimension=dimension, intervals=list(intervals), type='interval')
    return self

  def like(self, dimension, pattern):
    self.v = self.form_obj(dimension=dimension, pattern=pattern, type="like")
    return self

  def reg(self, dimension, pattern):
    self.v = self.form_obj(dimension=dimension, pattern=pattern, type="regex")
    return self

  def __and__(self, other):
    if self._logic is None:
      self_v = [self.v]
    elif self._logic == 'and':
      self_v = self.v
    else:
      raise APIException("API doesn't accept mixed logic")
    other_v = [other.v]
    fields = self_v + other_v
    self.v = fields
    self._logic = 'and'
    return self

  def __or__(self, other):
    if self._logic is None:
      self_v = [self.v]
    elif self._logic == 'or':
      self_v = self.v
    else:
      raise APIException("API doesn't accept mixed logic")
    other_v = [other.v]
    fields = self_v + other_v
    self.v = fields
    self._logic = 'or'
    return self

  def __invert__(self):
    if self._logic is None:
      field = self.v
      self.v = field
      self._logic = 'not'
      return self

class Filter:
  def __init__(self):
    pass

  def selector(self, dimension: str, value:str, extraction_fn=None):
    filter = LogicFilter()
    filter.selector(dimension=dimension, value=value, extraction_fn=extraction_fn)
    return filter

  def in_filter(self, *values, dimension: str):
    filter = LogicFilter()
    filter.in_filter(*values, dimension=dimension)
    return filter

  def bound(self,dimension, lower, ordering, upper=None, **kwargs):
    filter = LogicFilter()
    filter.bound(dimension=dimension, lower=lower, ordering=ordering,upper=upper, **kwargs)
    return filter

  def interval(self,*intervals, dimension: str):
    filter = LogicFilter()
    filter.interval(*intervals, dimension=dimension)
    return filter

  def like(self, dimension, pattern):
    filter = LogicFilter()
    filter.like(dimension=dimension, pattern=pattern)
    return filter

  def reg(self, dimension, pattern):
    filter = LogicFilter()
    filter.reg(dimension=dimension, pattern=pattern)
    return filter