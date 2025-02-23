import inspect
import sys


class Switch(object):
  def __init__(self, value):
    self.__case_factory = _case(value)
    
  def __enter__(self):
    return self.__case_factory
    
  def __exit__(self, exc_type, exc_value, traceback):
    pass
  
def _case(value):
  class _Case(object):
    def __init__(self, value, values, all_invalid, callback):
      self.__failed_match = value not in values
      
      callback(all_invalid and self.__failed_match)
      
    def __enter__(self):
      if self.__failed_match:
        sys.settrace(lambda *args, **keys: None)
        frame = inspect.currentframe().f_back
        frame.f_trace = self.__trace
        
    def __exit__(self, exc_type, exc_value, traceback):
      if self.__failed_match:
        return True
        
    def __trace(self, exc_type, exc_value, traceback):
      raise AttributeError('Case unmatched.')
      

  class _CaseFactory(object):
    def __init__(self, value):
      self.__value = value
      self.__values = []
      self.__all_invalid = True
       
    def __call__(self, value):
      if self.__all_invalid is None:
        raise self.__exception()
      
      self.__values = [value]
      
      return _Case(self.__value, self.__values, self.__all_invalid, self.__set_all_invalid)
      
    @staticmethod
    def __exception():
      return Exception('Default has been called, no more cases allowed.')
      
    def __set_all_invalid(self, invalid):
      self.__all_invalid = invalid
       
    def default(self):
      if self.__all_invalid:
        self.__values = [self.__value]
      else:
        self.__values = []
        
      self.__all_invalid = None
        
      return _Case(self.__value, self.__values, self.__all_invalid, self.__set_all_invalid)
    
    def fall(self, value):
      if self.__all_invalid is None:
        raise self.__exception()
      
      self.__values.append(value)

      return _Case(self.__value, self.__values, self.__all_invalid, self.__set_all_invalid)
      
  return _CaseFactory(value)
