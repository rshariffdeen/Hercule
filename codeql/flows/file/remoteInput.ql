/**
 * @name remote-to-file
 * @description detects if remote sources are used to write to files
 * @Author Ridwan Shariffdeen
 * @kind problem
 * @id py/remote-to-file
 * @security-severity 7.0
 * @problem.severity warning
 * @example-packages  zlibsrc-0.0.1
 * @tags remote content
 *       string consts
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources
import semmle.python.Concepts
import semmle.python.ApiGraphs

module RemoteToFileConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    sink = API::moduleImport("socket").getMember(_).getACall() or
      sink = API::moduleImport("requests").getMember(_).getACall() or
      sink = API::moduleImport("urlrequest").getMember(_).getACall() or
      sink = API::moduleImport("urllib3").getMember(_).getACall() or
      sink = API::moduleImport("httpx").getAMember().getACall()
  }

  predicate isSink(DataFlow::Node sink) {
    sink = any(FileSystemAccess fa).getAPathArgument() or
      sink.(DataFlow::CallCfgNode)
          .getFunction()
          .toString()
          .regexpMatch(".*(write|dumps?).*") or
      sink.(DataFlow::MethodCallNode)
          .getMethodName()
          .regexpMatch(".*(write|dumps?).*")

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
    TaintTracking::localTaint(nodeFrom, nodeTo)
  }

}

module RemoteToFileFlow = TaintTracking::Global<RemoteToFileConfiguration>;

from DataFlow::Node input, DataFlow::Node fileAccess
where RemoteToFileFlow::flow(input, fileAccess) and
  MyFlowConfiguration::isSource(input) and
  MyFlowConfiguration::isSink(fileAccess)
select input,  "remote content from " + input.getLocation() + " flowing to file content in " + fileAccess.getLocation()
