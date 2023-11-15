/**
 * @name dunder file Manipulation
 * @description Using __file__ can be risky
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/dunder-manipulation
 * @tags security
 */
import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::AttrRead p, DataFlow::ExprNode o
where
  p.accesses(o, "__file__")
select p.getLocation(), "Found a read of __file__"