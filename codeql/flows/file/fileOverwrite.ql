/**
 * @name File overwrite
 * @description The same file is being manipulated by reading and then writing to it
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/file-overwrite
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::Node p, DataFlow::CallCfgNode read, DataFlow::CallCfgNode write
where
  read != write and
  (
    read = API::builtin("open").getACall() or
    read = API::moduleImport("os").getMember("open").getACall()
  ) and
  (
    write = API::builtin("open").getACall() or
    write = API::moduleImport("os").getMember("open").getACall()
  ) and
  (
    TaintTracking::localTaint(p, read.getArg(_)) or
    TaintTracking::localTaint(p, read.getArgByName(_))
  ) and
  (
    TaintTracking::localTaint(p, write.getArg(_)) or
    TaintTracking::localTaint(p, write.getArgByName(_))
  )
  and
  (
    (read.getLocation().getFile() != write.getLocation().getFile())
    or (read.getLocation().getStartLine() <= write.getLocation().getStartLine())
  )
select p.getLocation(), "Found a read  at (" + read.getLocation() + ") and a write at (" + write.getLocation() + ") for " + p.getLocation() + "."