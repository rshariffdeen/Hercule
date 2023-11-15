/**
 * @name Strings
 * @description Listing strings
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/open-issues
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from StringValue s, DataFlow::CallCfgNode call
where
  s.getText().matches("%=")
  and call = API::moduleImport("base64").getMember("b64decode").getACall()
  and call.getArg(_).asCfgNode() = s.getAReference()
select s.getAReference().getLocation(), "Found string " + s.getText()
