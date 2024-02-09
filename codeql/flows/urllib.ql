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
 
 from DataFlow::CallCfgNode call
 where
   call = API::moduleImport(_).getMember("request").getMember(_).getACall() 
   or
   call = API::moduleImport(_).getMember("Request").getMember("urlopen").getACall() 
   or
   call = API::moduleImport(_).getMember("urlopen").getACall()  
 select call.getLocation(), "Found a read of urllib which is suspicious"
 