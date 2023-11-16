/**
 * @name Taint tracking of Sys field
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/sys-smarter
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    API::moduleImport("sys").getAMember().asSource() = source or
    API::moduleImport("sys").getAMember().getACall() = source
  }

  predicate isSink(DataFlow::Node sink) { any() }

  predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(DataFlow::ExprNode expr | expr = nodeTo |
      expr.asCfgNode().getAChild() = nodeFrom.asCfgNode()
    )
    or
    TaintTracking::localTaint(nodeFrom, nodeTo)
  }
}

module MyFlow = DataFlow::Global<MyFlowConfiguration>;

from DataFlow::Node read, DataFlow::ParameterNode p
where
  (
    API::moduleImport("sys").getAMember().asSource() = read
    or
    API::moduleImport("sys").getAMember().getACall() = read
  ) and
  MyFlow::flow(read, p)
select read.getLocation(), "sys data is used at " + p.getLocation().toString()
