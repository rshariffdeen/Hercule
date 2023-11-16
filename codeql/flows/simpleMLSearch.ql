/**
 * @name Machine learning strings
 * @description Usage of suspicious strings
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/ml-search-simple
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from StringValue s
where
  exists(string a |
    a in [
        "torch", "torchvision", "datasets", "tranformers", "huggingface_hub", "numpy", "scipy",
        "keras", "pandas", "tensorflow", "nltk", "theano", "resnet"
      ]
  |
    s.getText().matches("%" + a + "%")
  ) and
  exists(DataFlow::CallCfgNode call, DataFlow::Node q |
    s.getAReference() = q.asCfgNode() and
    (
      TaintTracking::localTaint(q, call.getArg(_)) or
      TaintTracking::localTaint(q, call.getArgByName(_))
    )
  )
select s.getAReference().getLocation(), "Found string " + s.getText()
