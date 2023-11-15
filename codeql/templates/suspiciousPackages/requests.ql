/**
 * @name Requests calls
 * @description Requests is a common library for network usage
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/dunder-manipulation
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 from DataFlow::CallCfgNode p
 where
   p = API::moduleImport("requests").getMember(_).getACall() 
 select p.getLocation(), "Found a read of requests"
 