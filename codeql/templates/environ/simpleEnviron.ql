/**
 * @name Simple usage of os.environ
 * @description Checking the local environment is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/environ-simple
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 
 from DataFlow::AttrRead read, DataFlow::Node p
 where
   read.accesses(API::moduleImport("os").asSource(),"environ") and
   TaintTracking::localTaint(read.getALocalSource(),p)
 select read.getLocation(),
   "Found a simple access to environ , which flows to " + p.getLocation().toString()
 