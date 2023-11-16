/**
 * @name Simple usage of os.environ through get
 * @description Checking the local environment is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/environ-simple-get
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 
 from DataFlow::CallCfgNode read, DataFlow::Node p
 where
   read = API::moduleImport("os").getMember("environ").getMember("get").getACall() and
   TaintTracking::localTaint(read.getALocalSource(),p)
 select read.getLocation(),
   "Found a simple get call to environ , which flows to " + p.getLocation()
 