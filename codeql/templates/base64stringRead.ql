/**
 * @name Finding base64 payload
 * @description Base64 payloads may be suspicious content
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/base64-string
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from StringValue s, DataFlow::CallCfgNode call, DataFlow::Node n
where
  s.getText().matches("%=") and
  call = API::moduleImport("base64").getMember("b64decode").getACall() and
  n.asCfgNode() = s.getAReference() and
  (
    call.getArg(_).asCfgNode() = s.getAReference() or
    call.getArgByName(_).asCfgNode() = s.getAReference() or
    TaintTracking::localTaint(n, call.getArg(_)) or
    TaintTracking::localTaint(n, call.getArgByName(_))
  )
select s.getAReference().getLocation(), "Found usage of a base64 string " + s.getText()
