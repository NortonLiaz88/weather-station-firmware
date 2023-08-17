#!/usr/bin/python
import rshell
rshell.copy_file('main.py', '/pyboard')
subprocess.call(["echo",""])

