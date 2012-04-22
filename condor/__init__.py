#!/usr/bin/env python

class CondorJob:
	""" Defines a condor job """

	def __init__(self,name):
		""" Constructor """
		self.name = name


	def script(self):
		""" Returns the condor script as a string """
		s = ""
		return s

	def write(self,jobfile):
		""" Writes job out to jobfile """
		f = open(jobfile,"w")
		f.write(self.script())
		f.close()

	def getName(self):
		""" Returns the job name """
		return self.name

	def submit(self):
		""" Submits job to condor """
		pass

class CondorJobNode(CondorJob):
	""" Represents a condor job node for use in a CondorDAG """

	children = []
	parents = []

	def pre(self,executable):
		""" sets the pre-executable for this node """
		pass

	def post(self,executable):
		""" sets the post-executable for this node """
		pass

	def getParents(self):
		""" Returns this nodes parents """
		return self.parents

	def getChildren(self):
		""" Returns this nodes children """
		return self.children

	def addParent(self,parent):
		""" Add a parent Job Node """
		parent.addChild(self)
		self.parents.append(parent)

	def addChild(self,child):
		""" Add a child Job Node """
		child.addParent(self)
		self.children.append(child)

	def before(self,beforenode):
		""" This node should complete before beforenode starts, alias for addChild """
		self.addChild(beforenode)

	def after(self,afternode):
		""" This node should start after afternode completes, alias for addParent """
		self.addParent(afternode)
		

class CondorDAG:
	""" Condor Job Graph, suitable for use with DAGman """
	nodelist = []

	def __init__(self):
		""" Constructor """
		pass

	def addNode(self,jobnode):
		""" Adds jobnode to nodelist """
		self.nodelist.append(jobnode)

	def script(self):
		""" Generates DAG Script """
		s = ""
		return s

	def write(self,dagfile):
		""" Writes dagfile """
		f = open(dagfile,"w")
		f.close()
		