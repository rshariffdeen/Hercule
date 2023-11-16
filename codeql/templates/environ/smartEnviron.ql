/**
 * @name Global taint tracking usage of os.environ
 * @description Checking the local environment is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/environ-smart
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    source.(DataFlow::AttrRead).accesses(API::moduleImport("os").asSource(), "environ")
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

from DataFlow::AttrRead read, DataFlow::Node p, string key
where
  (
    read.accesses(API::moduleImport("os").getMember("environ").asSource(), key) and
    MyFlow::flow(read, p)
  )
  or
  (
    read.accesses(API::moduleImport("os").getMember("environ").asSink(), key) and
    MyFlow::flow(p, read)
  ) 
  and
  not p.getLocation().getFile().inStdlib()
select read.getLocation(), "Flow between os.environ and " + p.getLocation()
