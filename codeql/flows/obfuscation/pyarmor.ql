/**
 * @name Usage of pyarmor
 * @description Using getattr is not common
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/pyarmor-ref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode call
where
  call = API::moduleImport(_).getMember("__pyarmor__").getACall() or
  call = API::moduleImport(_).getMember("pyarmor_runtime").getACall() or
  call = API::moduleImport(_).getMember("pyarmor_runtime_000000").getACall()
select call.getLocation(), "Found a read of pyarmor"