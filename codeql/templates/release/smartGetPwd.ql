/**
 * @name pwd.getpwuid smarter issues
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/pwuid
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

  predicate isSink(DataFlow::Node sink) { any() }

  predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    // exists(DataFlow::CallCfgNode call | call = nodeTo |
    //   (
    //     call = API::builtin(["chr", "ord"]).getACall()
    //     or
    //     call.getFunction().asCfgNode().(NameNode).getId() in ["chr", "ord"]
    //   ) and
    //   nodeFrom in [
    //       call.getArg(0), call.getArgByName("object"), call.getArgByName("chr"),
    //       call.getArgByName("number")
    //     ]
    // )
    // or
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
  call = API::moduleImport("pwd").getMember("getpwuid").getACall() and
  read.accesses(call, "pw_name") and
  MyFlow::flow(read, p) and
  p instanceof DataFlow::MethodCallNode and
  p.(DataFlow::MethodCallNode).calls(_, "sendall")
select call.getLocation(), "smart getPwuid data is used at $@", p.getLocation(), "  "
