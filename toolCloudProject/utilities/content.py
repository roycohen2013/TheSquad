#!/usr/bin/env python

defaults = {
	'heading' : "ToolCloud",
	'name' : "Anonymous"
}

def getDefaults():
	return defaults

def replace(key, newValue):
	for k in self.dict.keys():
		if k == key:
			self.dict[key] = newValue
