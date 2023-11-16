/**
 * @name simple pwd.getpwuid issues
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/pwuid-simple
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts



from
  DataFlow::CallCfgNode call, DataFlow::Node p, DataFlow::AttrRead read
where
  call = API::moduleImport("pwd").getMember("getpwuid").getACall() and
  read.accesses(call, _) and
  TaintTracking::localTaint(read.getALocalSource(), p)
  and p instanceof DataFlow::CallCfgNode
  and not p.getLocation().getFile().inStdlib()
select call.getLocation(), "simple getPwuid data is used at $@", p.getLocation(), "."
