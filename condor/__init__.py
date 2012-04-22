#!/usr/bin/env python

class CondorJob:
	""" Defines a condor job """

	def __init__(self,name):
		""" Constructor """
		self.jobfile = None
		self.name = name
		self.executable = None
		self.outputfile = "%s.out.$(Cluster)" % self.name
		self.errorfile = "%s.err.$(Cluster)" % self.name
		self.logfile = "%s.log.$(Cluster)" % self.name
		self.universe = "vanilla"
		self.arguments = []

	def setExecutable(self,executable):
		""" executable is the path to the program this job will run """
		self.executable = executable

	def setOutputfile(self,outputfile):
		"""The file job output should be written to"""
		self.outputfile = outputfile

	def setErrorfile(self,errorfile):
		""" The file that job errors should be written to"""
		self.errorfile = errorfile

	def setLogfile(self,logfile):
		""" The file that job logs should be written to"""
		self.errorfile = logfile

	def script(self):
		""" Returns the condor script as a string """
		s = ""
		s += "Executable = %s" % self.executable
		s += ""
		return s

	def write(self,jobfile):
		""" Writes job out to jobfile """
		f = open(jobfile,"w")
		f.write(self.script())
		f.close()
		self.jobfile = jobfile

	def getJobfile(self):
		return self.jobfile

	def getName(self):
		""" Returns the job name """
		return self.name

	def submit(self):
		""" Submits job to condor """
		pass

class CondorJobNode(CondorJob):
	""" Represents a condor job node for use in a CondorDAG """

	def __init__(self,name):
		""" Constructor """
		CondorJob.__init__(self,name)
		self.children = []
		self.parents = []

	def pre(self,executable,args):
		""" sets the pre-executable for this node """
		pass

	def post(self,executable,args):
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
		if parent not in self.parents:
			self.parents.append(parent)
			parent.addChild(self)

	def addChild(self,child):
		""" Add a child Job Node """
		if child not in self.children:
			self.children.append(child)
			child.addParent(self)


class CondorDAG:
	""" Condor Job Graph, suitable for use with DAGman """

	def __init__(self):
		""" Constructor """
		self.nodelist = []

	def addNode(self,jobnode):
		""" Adds jobnode to nodelist """
		self.nodelist.append(jobnode)

	def script(self):
		""" Generates DAG Script """
		s = ""
		for node in self.nodelist:
			s += "JOB %s %s\n" % (node.getName(),node.getJobfile())

		for node in self.nodelist:
			children = node.getChildren()
			if len(children) > 0:
				childnames = map(lambda x: x.getName(),children)
				s += "PARENT %s CHILD %s\n" % (node.getName(),",".join(childnames))

		return s

	def write(self,dagfile):
		""" Writes dagfile """
		f = open(dagfile,"w")
		f.write(self.script())
		f.close()
		
