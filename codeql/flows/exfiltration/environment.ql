/**
 * @name environment-to-remote
 * @description a data flow exist from environment variable to a remote endpoint
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/environment-to-remote
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    source = API::moduleImport("os").getMember("environ").asSource()
    or source = API::moduleImport("os").getMember("environ").getMember("get").getACall() or
    source.(DataFlow::AttrRead).accesses(API::moduleImport("os").getMember("environ").asSource(), _) 
  }

  predicate isSink(DataFlow::Node sink) { 
    (
    sink = API::moduleImport("socket").getMember(_).getACall() or
    sink = API::moduleImport("requests").getMember("get").getACall() or
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
  MyFlowConfiguration::isSink(sink)
  and sink != source
select sink.getLocation(), "environment data flows from " + source.getLocation() + " to " + sink.getLocation()