/**
 * @name dunder file Manipulation
 * @description Using __file__ can be risky
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/get-attr-dunder-file
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode call, DataFlow::CallCfgNode source
where
  call = API::builtin("getattr").getACall() and
  source.asExpr().getAChildNode().(StringPart).getText() = "__file__" and
  TaintTracking::localTaint(source.getALocalSource(), call.getArg(_))
select call.getLocation(), "Found a read of __file__ at " + call.getLocation()
