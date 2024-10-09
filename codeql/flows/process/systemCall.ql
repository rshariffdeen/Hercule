/**
 * @name a remote end point influences a system process call
 * @description a data flow exist to system process call from a remote endpoint
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/remote-to-process
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSink(DataFlow::Node source) {
    source = API::moduleImport("subprocess").getMember(_).getACall() 
    or source = API::moduleImport("os").getMember("system").getACall()
  }

  predicate isSource(DataFlow::Node sink) {
    (
    sink = API::moduleImport("socket").getMember(_).getACall() or
    sink.(DataFlow::CallCfgNode).getFunction().toString().regexpMatch(".*(request|sendall|connect|urlretrieve|urlopen|send|post|put|patch|delete|get?).*") or
    sink.(DataFlow::MethodCallNode).getMethodName()      .regexpMatch(".*(request|sendall|connect|urlretrieve|urlopen|send|post|put|patch|delete|get?).*"))
    and not sink.getLocation().getFile().inStdlib()
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
select sink.getLocation(), "remote end point influence system call, from " + source.getLocation() + " to " + sink.getLocation()
