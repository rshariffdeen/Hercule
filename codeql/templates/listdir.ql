/**
 * @name Os.listdir calls
 * @description Using listdir can be a sign of dynamic behavior
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/list-dir
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from DataFlow::CallCfgNode call, DataFlow::ParameterNode p
where
  call = API::moduleImport("os").getMember("listdir").getACall() and
  TaintTracking::localTaint(p, call.getArg(_))
  or
  TaintTracking::localTaint(p, call.getArgByName(_))
select call.getLocation(), "Found a flow from " + p.getLocation() + " to os.listdir"
