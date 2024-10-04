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

module RemoteToFileConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  predicate isSink(DataFlow::Node sink) {
    sink = any(FileSystemAccess fa).getAPathArgument()
  }
}

module RemoteToFileFlow = TaintTracking::Global<RemoteToFileConfiguration>;

from DataFlow::Node input, DataFlow::Node fileAccess
where RemoteToFileFlow::flow(input, fileAccess)
select input,  "This file " + fileAccess + " access uses data from $@." +
  input +  "user-controllable remote input."