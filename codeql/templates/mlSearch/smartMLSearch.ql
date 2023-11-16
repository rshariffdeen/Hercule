/**
 * @name smartML search
 * @description Usage of suspcious strings with global taint tracking
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/ml-search-smart
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

predicate referencesModule(Expr e) {
  exists(string x |
    e.getAChildNode().(StringPart).getText().matches("%" + x + "%") and
    x in [
        "torch", "torchvision", "datasets", "tranformers", "huggingface_hub", "numpy", "scipy",
        "keras", "pandas", "tensorflow", "nltk", "theano"
      ]
  )
}

module MyFlowConfiguration implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) { referencesModule(source.asExpr()) }

  predicate isSink(DataFlow::Node sink) { any() }

  predicate isAdditionalFlowStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    exists(DataFlow::ExprNode expr | expr = nodeTo |
      expr.asCfgNode().getAChild() = nodeFrom.asCfgNode()
    )
    or
    TaintTracking::localTaint(nodeFrom, nodeTo)
  }
}

module MyFlow = DataFlow::Global<MyFlowConfiguration>;

from DataFlow::ExprNode p, StringValue s
where
  exists(string a |
    a in [
        "torch", "torchvision", "datasets", "tranformers", "huggingface_hub", "numpy", "scipy",
        "keras", "pandas", "tensorflow", "nltk", "theano", "resnet"
      ]
  |
    s.getText().matches("%" + a + "%")
  ) and
  p.asExpr().refersTo(s.getAReference())
select s.getAReference().getLocation(), "Found string " + s.getText() + "and it flows to ($@)",
  p.getLocation(), "."
// from DataFlow::ExprNode literal, DataFlow::Node p
// where
//   referencesModule(literal.asExpr()) and
//   MyFlow::flow(literal, p)
// select literal.getLocation(), "flow between a suspicious string and $@", p.getLocation(), "  "
