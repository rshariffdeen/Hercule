/**
 * @name Pathlib reference
 * @description Pathlib is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/pathlib-ref
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 from DataFlow::CallCfgNode p
 where
   p = API::moduleImport(_).getMember("pathlib").getMember(_).getACall()
   and not p.getLocation().getFile().inStdlib() 
 select p.getLocation(), "Found a read of pathlib which is suspicious"
 