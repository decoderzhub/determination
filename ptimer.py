import threading
from threading import Timer,Thread,Event,RLock


class perpetualTimer(object):

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      with RLock():
         self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    print('ipsem lorem')

# t = perpetualTimer(5,printer)
# t.start()