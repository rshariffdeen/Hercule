/**
 * @name Using of the marshal package
 * @description Malicious code can be read from it
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
 
 from DataFlow::AttrRead read, DataFlow::ParameterNode p
 where
   read.accesses(API::moduleImport("marshal").asSource(), _) and
   TaintTracking::localTaint(read.getALocalSource(), p)
 select read.getLocation(), "Found a call to a marshal field, which flows to $@", p.getLocation(), "."
 