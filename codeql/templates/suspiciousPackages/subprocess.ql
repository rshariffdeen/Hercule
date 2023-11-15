/**
 * @name Invocation of subprocess is suspicious
 * @description Subprocess is not a commonly used package
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
  p = API::moduleImport("subprocess").getAMember().getACall()
select p.getLocation(), "Found a call of a subprocess field"