/**
 * @name Get pass flows to an external write
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/getpass-flow
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    source = API::moduleImport("getPass").getMember(_).asSource()
  }

  predicate isSink(DataFlow::Node sink) {
    (
      sink = API::moduleImport("socket").getMember(_).getACall() or
      sink.(DataFlow::CallCfgNode)
          .getFunction()
          .toString()
          .regexpMatch(".*(write|sendall|send|post|put|patch|delete|get|exec|eval?).*") or
      sink.(DataFlow::MethodCallNode)
          .getMethodName()
          .regexpMatch(".*(write|sendall|send|post|put|patch|delete|get|exec|eval?).*")
    ) and
    not sink.getLocation().getFile().inStdlib()
  }

  predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(DataFlow::ExprNode expr | expr = nodeTo |
      expr.asCfgNode().getAChild() = nodeFrom.asCfgNode()
    )
    or
    TaintTracking::localTaint(nodeFrom, nodeTo)
  }
}

module MyFlow = DataFlow::Global<MyFlowConfiguration>;

from DataFlow::Node sink, DataFlow::Node source
where
  MyFlowConfiguration::isSource(source) and
  MyFlow::flow(source, sink) and
  MyFlowConfiguration::isSink(sink) and
  sink != source
select sink.getLocation(), "GetPass data is used at " + sink.getLocation()