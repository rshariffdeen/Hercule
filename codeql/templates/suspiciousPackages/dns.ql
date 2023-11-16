/**
 * @name Invocation of dns is suspicious
 * @description DNS is not commonly manipulated
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/dns-ref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("dns").getAMember().getACall()
  or p = API::moduleImport("dns").getAMember().getAMember().getACall()
select p.getLocation(), "Found a reference of the dns module"