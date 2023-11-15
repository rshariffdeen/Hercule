/**
 * @name Os.open calls
 * @description Using os.open is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/open-issues
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from DataFlow::CallCfgNode call, DataFlow::ParameterNode p
where
  call = API::moduleImport("os").getMember("open").getACall() and

  TaintTracking::localTaint(p, call.getArg(_)) or TaintTracking::localTaint(p,call.getArgByName(_))
select call.getLocation(), "Found a call to open with a controlled argument"