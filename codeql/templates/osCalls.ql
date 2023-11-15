/**
 * @name Invocation of some calls of the os package is suspicious
 * @description Using __import__ is not common
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
  p = API::moduleImport("os").getMember("add_dll_directory").getACall()
  or  p = API::moduleImport("os").getMember("add_dll_directory").getACall()
  or  p = API::moduleImport("os").getMember("listdir").getACall() 
  or  p = API::moduleImport("os").getMember("walk").getACall() 
  or  p = API::moduleImport("os").getMember("popen").getACall()
  or  p = API::moduleImport("os").getMember("rename").getACall()
  or  p = API::moduleImport("os").getMember("startfile").getACall()
  or  p = API::moduleImport("os").getMember("uname").getACall()

  
select p.getLocation(), "Found a usage of a commonly targetted os call"