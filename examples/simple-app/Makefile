# Set the name of your application:
APPLICATION = simple-app

# If no BOARD is found in the environment, use this default:
# BOARD ?= nucleo-f401re
BOARD ?= native

# Use our benchmarking module
USEMODULE += bench_context_switching
USEMODULE += xtimer

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(CURDIR)/../..
include $(RIOTBASE)/Makefile.include
