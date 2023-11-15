/**
 * @name Invocation of browsercookie
 * @description Browsercookie is bad
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/browsercookie0-reference
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("browser_cookie3").getAMember().getACall()
select p.getLocation(), "Found a reference of browser_cookie3"