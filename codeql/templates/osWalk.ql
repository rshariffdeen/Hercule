/**
 * @name Os.walk calls
 * @description Os.walk is not commonly used and can leak a lot of information 
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/os-walk
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from DataFlow::CallCfgNode call, DataFlow::ParameterNode p
where
  call = API::moduleImport("os").getMember("walk").getACall() and
  TaintTracking::localTaint(p, call.getArg(_)) or TaintTracking::localTaint(p,call.getArgByName(_))
select call.getLocation(), "Found a call to os.walk"