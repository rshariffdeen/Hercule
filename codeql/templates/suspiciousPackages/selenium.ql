/**
 * @name Reference of the selenium package
 * @description Selenium can be used to get a payload
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/dunder-manipulation
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::CallCfgNode p
where
  p = API::moduleImport("selenium").getAMember().getACall()
select p.getLocation(), "Found a read of selenium"