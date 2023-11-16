/**
 * @name Invocation of some calls of the os package is suspicious
 * @description Using some specific os functionality may be a flag for suspicious behavior
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/os-calls
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p, string x
where
  x in ["add_dll_directory", "listdir", "walk", "popen", "rename", "startfile", "uname"] and
  p = API::moduleImport("os").getMember(x).getACall()
select p.getLocation(), "Found a usage of a commonly targetted os call " + x
