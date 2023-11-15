/**
 * @name Invocation of base64
 * @description Payloads commonly come in base64
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/base64ref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("base64").getAMember().getACall()
select p.getLocation(), "Found a reference of base64"