#!/usr/bin/env python

"""

utils: part of the pyneurovault package

pyneurovault: a python wrapped for the neurovault api

"""

import os
import json
import errno
import urllib2
import numpy as np
from pandas.io.json import read_json
from urllib2 import Request, urlopen, HTTPError

__author__ = ["Poldracklab","Chris Filo Gorgolewski","Gael Varoquaux","Vanessa Sochat"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/01/16 $"
__license__ = "BSD"


# File operations 

def mkdir_p(path):
  try:
      os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

def url_get(url):
  request = Request(url)
  response = urlopen(request)
  return response.read()

# Data Json Object

class DataJson:
  """DataJson: internal class for storing json, accessed by NeuroVault Object"""
  def __init__(self,url):
    self.url = url
    self.json = self.__get_json__()
    self.data = self.__parse_json__() 
    
  """Print json data fields"""
  def __str__(self):
    return "DataJson Object dj Includes <dj.data:pandas,dj.json:list,dj.url:str>"

  """Get raw json object"""
  def __get_json__(self):
    json = urllib2.urlopen(self.url).read()
    return json.decode("utf-8")
    
  """Parse a json object into a dictionary (key = fields) of dictionaries (key = file urls)"""
  def __parse_json__(self):
    if not self.json:
      self.json = self.__get_json__()
    data = read_json(self.json)
    if data.empty: 
      print "Warning, %s is not in NeuroVault!" %(self.url)
      return None
    else: return data

  def __get_fields__(self):
    return list(self.data.columns)
