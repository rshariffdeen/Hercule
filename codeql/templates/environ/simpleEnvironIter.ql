/**
 * @name Simple iteration of os.environ
 * @description Checking the local environment through an iteration is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/environ-iter
 * @tags security
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 
 
 from DataFlow::IterableSequenceNode read, DataFlow::Node p
 where
   read = API::moduleImport("os").getMember("environ").asSource()
 select read.getLocation(),
   "Found a simple iteration of environ, which flows to " + p.getLocation()
 