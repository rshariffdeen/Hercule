/**
 * @name Urlrlib invocation
 * @description Mentioning of urllib is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/urlib-ref
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 from DataFlow::CallCfgNode p
 where
   p = API::moduleImport(_).getMember("request").getMember(_).getACall() 
   or
   p = API::moduleImport(_).getMember("Request").getMember("urlopen").getACall() 
   or
   p = API::moduleImport(_).getMember("urlopen").getACall()  
 select p.getLocation(), "Found a read of urllib which is suspicious"
 