import tracemalloc
from datetime import timedelta
import time
import os

def startLog(logDataDict, file):
  logDataDict.update({'start_time': time.perf_counter()})
  logDataDict.update({'start_file_size': round(os.path.getsize(file)/1000000, 2)})
  tracemalloc.start()
  return logDataDict

def endLog(logDataDict, faFileNameExt, squeakyFile):
  logDataDict.update({'file_name': faFileNameExt})
  logDataDict.update({'end_file_size': round(os.path.getsize(squeakyFile)/1000000, 2)})
  logDataDict.update({'memory': round(tracemalloc.get_traced_memory()[1]/1000000, 2)})
  tracemalloc.stop()
  logDataDict.update({'end_time': time.perf_counter()})
  duration = timedelta(seconds=logDataDict['end_time'] - logDataDict['start_time'])
  logDataDict.update({'duration': str(duration)})
  return logDataDict
