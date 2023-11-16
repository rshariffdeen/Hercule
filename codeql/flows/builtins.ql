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

from DataFlow::CallCfgNode p, string x
where
  p = API::builtin(x).getACall() and
  x in ["compile", "__import__", "globals", "vars"] and
  not p.getLocation().getFile().inStdlib()
select p.getLocation(), "Found a read of a suspicious builtin " + x
