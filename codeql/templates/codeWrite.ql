/**
 * @name Reading __code__
 * @description Using some builtins is not common
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/read-dunder-code
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 from DataFlow::AttrWrite write
 where
   write.accesses(_, "__code__")
 select write.getLocation(), "Found a write of the __code__ field in the function " + write.getEnclosingCallable().getQualifiedName()
 