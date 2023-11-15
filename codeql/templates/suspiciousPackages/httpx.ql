/**
 * @name Reference of httpx
 * @description Httpx may be used as a remote file source
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/httpxref
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("httpx").getAMember().getACall()
select p.getLocation(), "Found a reference of httpx"