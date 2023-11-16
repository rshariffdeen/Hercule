/**
 * @name Invocation of getpass
 * @description Using getpass is not common
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/getpass-reference
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("getpass").getAMember().getACall()
select p.getLocation(), "Found a read of getattr"