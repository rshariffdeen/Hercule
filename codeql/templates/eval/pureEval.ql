/**
 * @name Detects any eval function call
 * @description The eval() function evaluates Python code represented as a string or masrhalled.
 * @author Fabian Froh
 * @kind problem
 * @id py/usage-of-eval
 * @problem.severity warning
 * @security-severity 5.0
 * @package-examples eslint-scope eslint-config-eslint 
 * @tags security 
 * eval
 * arbitrary_code_execution
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs

 from DataFlow::CallCfgNode e
 where e = API::builtin("eval").getACall() or e = API::builtin("exec").getACall()
 select e, "Found use of direct eval or exec with argument ($@) in code.", e, e.getArg(0).getLocation().toString()