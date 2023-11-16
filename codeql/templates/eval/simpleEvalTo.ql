/**
 * @name eval and eval_literal from calls
 * @description Tracking flow from an eval to a value
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/eval-simple-from
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

predicate isEvalCall(DataFlow::CallCfgNode call) {
  call = API::builtin("eval").getACall() or
  call = API::builtin("exec").getACall() or
  call = API::moduleImport("ast").getMember("literal_eval").getACall()
}

from DataFlow::CallCfgNode call, DataFlow::ParameterNode p
where
  isEvalCall(call) and
  TaintTracking::localTaint(p, call)
select call, "Evaluation called with argument ($@)", p, p.asExpr().toString()
