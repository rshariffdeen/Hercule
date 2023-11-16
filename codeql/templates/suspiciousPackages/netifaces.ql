/**
 * @name Usage of netifaces 
 * @description Netifaces is an old package, which access to interfaces. This is not common behavior
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/netifaces-ref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("netifaces").getAMember().getACall()
select p.getLocation(), "Found a read of netifaces"