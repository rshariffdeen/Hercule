/**
 * @name Invocation of ssl is suspicious
 * @description SSL should not generally be touched
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/ssl-ref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("ssl").getAMember().getACall()
select p.getLocation(), "Found a read of ssl"