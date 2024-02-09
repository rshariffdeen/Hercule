/**
 * @name Invocation of special builtins
 * @description Using some builtins is not common
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/builtins
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode call, string name
where
  call = API::builtin(name).getACall() and
  name in ["compile", "__import__", "globals", "vars"] and
  not call.getLocation().getFile().inStdlib()
select call.getLocation(), "Found a read of a suspicious builtin " + name
