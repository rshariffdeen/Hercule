/**
 * @name Invocation of socket is suspicious
 * @description Sockets are not commonly used
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/socket-ref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("socket").getAMember().getACall()
select p.getLocation(), "Found a read of socket"