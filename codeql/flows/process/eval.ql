/**
 * @name Eval/exec flows to an external write
 * @description smth
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/eval-flow
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 import semmle.python.Concepts
 
 module MyFlowConfiguration implements DataFlow::ConfigSig {
   predicate isSource(DataFlow::Node source) {
     source = API::builtin("eval").getACall() 
     or source = API::builtin("exec").getACall()
     or source = API::moduleImport("ast").getMember("literal_eval").getACall()
   }
 
   predicate isSink(DataFlow::Node sink) { 
     (
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
 
 from DataFlow::Node sink, DataFlow::Node source
 where
   MyFlowConfiguration::isSource(source) and
   MyFlow::flow(source, sink) and 
   MyFlowConfiguration::isSink(sink)
   and sink != source
 select sink.getLocation(), "Evaluation data flows from " + source.getLocation() + " to " + sink.getLocation()
 