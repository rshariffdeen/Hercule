/**
 * @name dunder file Manipulation
 * @description Using __file__ can be risky
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

from DataFlow::CallCfgNode p, DataFlow::CallCfgNode q
where
  p = API::builtin("getattr").getACall() and
  q.asExpr().getAChildNode().(StringPart).getText() = "__file__" and
  TaintTracking::localTaint(q.getALocalSource(), p.getArg(1))
select p.getLocation(), "Found a read of __file__"
