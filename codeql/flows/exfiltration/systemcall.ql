/**
 * @name system-call-to-remote
 * @description data flow from sensitive API calls to a remote endpoint
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/system-call-to-remote
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
      source = API::moduleImport("socket").getMember("gethostname").getACall() or
      source = API::moduleImport("getpass").getMember(_).getACall() or
      source = API::moduleImport("pwd").getMember("getpwuid").getACall()
  }

  predicate isSink(DataFlow::Node sink) { (
     (
       exists(string name |
         sink = API::moduleImport("os").getMember(name).getACall() and
         name in ["add_dll_directory", "popen", "Popen", ""rename", "startfile", "uname"]
       )
       or
       sink instanceof SystemCommandExecution
     ) and
     not sink.getLocation().getFile().inStdlib()
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
select source, "sensitive data is extracted from " + source.getLocation() + " into "  + sink.getLocation()

from DataFlow::Node sink, DataFlow::Node source
where
  MyFlowConfiguration::isSink(sink)
select sink, "sensitive data is extracted to " + sink.getLocation()

