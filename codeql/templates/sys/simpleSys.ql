/**
 * @name sys readings
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/open-issues
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::Node read, DataFlow::ParameterNode p
where
  (
    read = API::moduleImport("sys").getAMember().asSource() or
    read = API::moduleImport("sys").getAMember().getACall()
  ) and
  TaintTracking::localTaint(read.getALocalSource(), p)
select read.getLocation(), "Found a call to a system field, which flows to $@", p.getLocation(), "."
