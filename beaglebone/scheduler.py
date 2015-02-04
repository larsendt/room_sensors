#!/usr/bin/env python

import time

class Scheduler(object):
    def __init__(self):
        self._functions = {}
        self._updates = {}
        self._cur_id = 0
        

    def add_function(self, fn, interval):
        self._functions[self._cur_id] = [fn, interval]
        self._updates[self._cur_id] = 0
        self._cur_id += 1


    def ping(self):
        for fn_id in self._functions:
            now = time.time()
            fn, interval = self._functions[fn_id]
            last_updated = self._updates[fn_id]

            if now > (last_updated + interval):
                fn()
                self._updates[fn_id] = time.time()
