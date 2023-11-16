/**
 * @name Marshal.loads calls
 * @description Marshal.loads can decode any code
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/marshal-loads
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from DataFlow::CallCfgNode call, DataFlow::ParameterNode p
where
  call = API::moduleImport("marshal").getMember("loads").getACall() and
  TaintTracking::localTaint(p, call.getArg(_)) or TaintTracking::localTaint(p,call.getArgByName(_))
  and not p.getLocation().getFile().inStdlib()
select call.getLocation(), "Found a call to marshal.loads with a controlled argument"