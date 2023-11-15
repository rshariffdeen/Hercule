/**
 * @name eval smarter issues from
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/pwuid
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    exists(DataFlow::CallCfgNode call |
      (
        call = API::builtin("eval").getACall() or
        call = API::builtin("exec").getACall() or
        call = API::moduleImport("ast").getMember("literal_eval").getACall()
      ) and
      source = call
    )
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

from DataFlow::CallCfgNode call, DataFlow::Node p
where
  (
    call = API::builtin("eval").getACall()
    or
    call = API::builtin("exec").getACall()
    or
    call = API::moduleImport("ast").getMember("literal_eval").getACall()
  ) and
  MyFlow::flow(call, p)
select call, "Evaluation flows into ($@)", p, p.asExpr().toString()
