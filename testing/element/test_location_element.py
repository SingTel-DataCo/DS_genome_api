__author__ = 'jingxuan'

import unittest
from genomeapi.elements.location import Location
from genomeapi.elements.exceptions import APIException

class TestLocation(unittest.TestCase):
  def test_location_au(self):
    loc = Location(country="AU")
    res = loc(location_type="locationHierarchyLevel", level_type='sa4', id='126')
    expected = {
      "location": {
        "locationType": "locationHierarchyLevel",
        "levelType": "sa4",
        "id": "126"
      }
    }
    self.assertEqual(res, expected)

  def test_location_sg(self):
    loc = Location(country="SG")
    res = loc(location_type="locationHierarchyLevel", level_type='staypoint_subzone', id='126')
    expected = {
      "location": {
        "locationType": "locationHierarchyLevel",
        "levelType": "staypoint_subzone",
        "id": "126"
      }
    }
    self.assertEqual(res, expected)

  def test_location_type_exception(self):
    loc = Location()
    with self.assertRaises(APIException) as context:
      loc(location_type="other", level_type='sa4', id='126')
    self.assertTrue("Sorry, we don't support this location type for now", str(context.exception))

  def test_location_level_exception(self):
    loc = Location()
    with self.assertRaises(APIException) as context:
      loc(location_type="locationHierarchyLevel", level_type='sa5', id='126')
    self.assertTrue("Sorry, we don't have such type for location", str(context.exception))

  def test_location_level_exception_for_origin(self):
    loc = Location()
    res = loc(location_type="locationHierarchyLevel", level_type='origin_sa4', id='126')
    expected = {
      "location": {
        "locationType": "locationHierarchyLevel",
        "levelType": "origin_sa4",
        "id": "126"
      }
    }
    self.assertEqual(res, expected)

  def test_location_with_direction(self):
    loc = Location()
    res = loc(location_type="locationHierarchyLevel", level_type='sa4', id='126', direction='origin')
    expected = {
      "location": {
        "locationType": "locationHierarchyLevel",
        "levelType": "origin_sa4",
        "id": "126",
      }
    }
    self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()