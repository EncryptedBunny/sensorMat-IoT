## Import needed modules from osc4py3
#from osc4py3.as_eventloop import *
#from osc4py3 import oscmethod as osm
#
#def handlerfunction(s, x, y):
#    # Will receive message data unpacked in s, x, y
#    pass
#
#def handlerfunction2(address, s, x, y):
#    # Will receive message address, and message data flattened in s, x, y
#    pass
#
## Start the system.
#osc_startup()
#
## Make server channels to receive packets.
#osc_udp_server("10.30.11.36", 12002, "hayballServer")
#
## Associate Python functions with message address patterns, using default
## argument scheme OSCARG_DATAUNPACK.
#osc_method("/q", handlerfunction)
## Too, but request the message address pattern before in argscheme
#osc_method("/test/*", handlerfunction2, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
#
## Periodically call osc4py3 processing method in your event loop.
#finished = False
#while not finished:
#    # …
#    osc_process()
#    # …
#
## Properly close the system.
#osc_terminate()

"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/q", print)
  dispatcher.map("/w", print)
  dispatcher.map("/e", print)
  dispatcher.map("/a", print)
  dispatcher.map("/s", print)
  dispatcher.map("/d", print)
  dispatcher.map("/z", print)
  dispatcher.map("/x", print)
  dispatcher.map("/c", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()