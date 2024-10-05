/**
 * @name dunder file overwrite
 * @description Using __file__ as an argument to a copy is a big issue
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

predicate isOSOpen(DataFlow::CallCfgNode call) {
  /* conservative open - any mode is suspicious */
  call = API::moduleImport("os").getMember("open").getACall()
}

predicate isSystemCall(DataFlow::CallCfgNode call) {
  call = API::moduleImport("os").getMember("system").getACall().getArg(0)
}

predicate isBuiltinOpen(DataFlow::CallCfgNode call) {
  call = API::builtin("open").getACall()
}

predicate isShutilCopy(DataFlow::CallCfgNode call) {
  call = API::moduleImport("shutil").getMember("copy").getACall() or
  call = API::moduleImport("shutil").getMember("copyfile").getACall() or
  call = API::moduleImport("shutil").getMember("copy2").getACall()
}

from DataFlow::AttrRead read, DataFlow::ExprNode obj, DataFlow::CallCfgNode call
where
  read.accesses(obj, "__file__") and
  (
    isOSOpen(call) or
    isBuiltinOpen(call) or
    isSystemCall(call) or
    isShutilCopy(call)
  ) and
  TaintTracking::localTaint(read.getALocalSource(), call)
select call.getLocation(), "Found a usage of __file__ $@ ", read.getLocation(), "."
