/**
 * @name file-to-remote
 * @description detects flows from files to remote end points
 * @Author Ridwan Shariffdeen
 * @kind problem
 * @id py/remote-to-file
 * @security-severity 7.0
 * @problem.severity warning
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
  predicate isSink(DataFlow::Node source) {
      sink = API::moduleImport("socket").getMember(_).getACall() or
      sink = API::moduleImport("requests").getMember(_).getACall() or
      sink = API::moduleImport("urlrequest").getMember(_).getACall() or
      sink = API::moduleImport("urllib3").getMember(_).getACall() or
      sink = API::moduleImport("httpx").getAMember().getACall()
  }

  predicate isSource(DataFlow::Node sink) {
    sink = any(FileSystemAccess fa).getAPathArgument() or
      sink.(DataFlow::CallCfgNode)
          .getFunction()
          .toString()
          .regexpMatch(".*(read?).*") or
      sink.(DataFlow::MethodCallNode)
          .getMethodName()
          .regexpMatch(".*(read?).*")

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
where RemoteToFileFlow::flow(fileAccess, input) and
  MyFlowConfiguration::isSource(fileAccess) and
    MyFlowConfiguration::isSink(input) and

select input,  "file content from " + file.getLocation() + " flowing to remote end point at " + input.getLocation()
