/**
 * @name pwd.getpwuid smarter issues
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/pwuid-smart
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    exists(DataFlow::CallCfgNode call |
      call = API::moduleImport("pwd").getMember("getpwuid").getACall() and
      source.(DataFlow::AttrRead).accesses(call, _)
    )
  }

  predicate isSink(DataFlow::Node sink) { (
    sink = API::moduleImport("socket").getMember(_).getACall() or
    sink.(DataFlow::CallCfgNode).getFunction().toString().regexpMatch(".*(write|sendall|send|post|put|patch|delete|get|exec|eval|dumps?).*") or
    sink.(DataFlow::MethodCallNode).getMethodName()      .regexpMatch(".*(write|sendall|send|post|put|patch|delete|get|exec|eval|dumps?).*"))
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

from DataFlow::CallCfgNode call, DataFlow::Node p, DataFlow::AttrRead read
where
  MyFlowConfiguration::isSource(read) and
  read.accesses(call, "pw_name") and
  MyFlow::flow(read, p)
select call.getLocation(), "smart getPwuid data is used at $@", p.getLocation(), "  "