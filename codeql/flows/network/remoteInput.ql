/**
 * @name Detects file writing from remote sources
 * @description detects if remote sources are used to write to files
 * @Author Ridwan Shariffdeen
 * @kind problem
 * @id py/remote-flow-to-file
 * @security-severity 7.0
 * @problem.severity high
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
    source = API::moduleImport("requests").getMember(_).getACall()
  }

  predicate isSink(DataFlow::Node sink) {
    sink = any(FileSystemAccess fa).getAPathArgument() or
      sink.(DataFlow::CallCfgNode)
          .getFunction()
          .toString()
          .regexpMatch(".*(write|dumps|system?).*") or
      sink.(DataFlow::MethodCallNode)
          .getMethodName()
          .regexpMatch(".*(write|dumps|system?).*")

  }
}

module RemoteToFileFlow = TaintTracking::Global<RemoteToFileConfiguration>;

from DataFlow::Node input, DataFlow::Node fileAccess
where RemoteToFileFlow::flow(input, fileAccess)
select input,  "Detected remote content from " + fileAccess.getLocation() + " flowing to file content in " +
  input.getLocation() +  " with a user-controllable remote input."
