/**
 * @name Base64 flows to an external write or system command
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/process-with-shell
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
  (
        exists(DataFlow::ArgumentNode a | a.toString().regexpMatch(".*(sh|powershell|curl|wget|nslookup?).*") | source.asCfgNode() = a.asCfgNode() )

  )
  and not source.getLocation().getFile().inStdlib()
  }

  predicate isSink(DataFlow::Node sink) {
    (
      sink = API::moduleImport("socket").getMember(_).getACall()   or
      sink.(DataFlow::CallCfgNode)
          .getFunction()
          .toString()
          .regexpMatch(".*(connect|sendall|send|post|put|patch|delete|get|exec|eval|compile?).*") or
      sink.(DataFlow::MethodCallNode)
          .getMethodName()
          .regexpMatch(".*(connect|sendall|send|post|put|patch|delete|get|exec|eval|compile?).*")
    )

    and not sink.getLocation().getFile().inStdlib()
  }

   predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(DataFlow::ExprNode expr | expr = nodeTo |
      expr.asCfgNode().getAChild() = nodeFrom.asCfgNode()
    )
    or
    exists(DataFlow::CallCfgNode call | call = nodeTo |
      call.getArgByName(_) = nodeFrom or
      call.getArg(_) = nodeFrom
    )
    or
    exists(DataFlow::MethodCallNode call | call = nodeTo |
      call.getArgByName(_) = nodeFrom or
      call.getArg(_) = nodeFrom
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
  MyFlowConfiguration::isSink(sink)
select source,
  "shell command flows from " + source.getLocation() + " to an execution " + sink.getLocation()

