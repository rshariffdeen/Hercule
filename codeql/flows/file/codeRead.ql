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
 
 from DataFlow::AttrRead read
 where
   read.accesses(_, "__code__")
 select read.getLocation(), "Found a read of the __code__ field in the function " + read.getEnclosingCallable().getQualifiedName()
 