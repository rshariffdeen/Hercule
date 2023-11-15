/**
 * @name Strings
 * @description Usage of suspicious strings
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

from StringValue s
where
  exists(string a |
    a in [
        "torch", "torchvision", "datasets", "tranformers", "huggingface_hub", "numpy", "scipy",
        "keras", "pandas", "tensorflow", "nltk", "theano", "resnet"
      ]
  |
    s.getText().matches("%" + a + "%")
  )
select s.getAReference().getLocation(), "Found string " + s.getText()
