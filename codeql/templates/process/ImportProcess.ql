/**
 * @name Require of child process
 * @description Detects if any child process is required as module
 * @author Martin Mirchev
 * @kind problem
 * @id py/require-child-process
 * @security-severity 3.0
 * @problem.severity warning
 * @example-packages kraken-api
 * @tags security
 * child_process
 * process
 * spwan
 * exec
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 import semmle.python.Concepts

 from Import r
 where r.getAnImportedModuleName().toString() = "subprocess" or r.getAnImportedModuleName().toString() = "os.system"
 and not r.getLocation().getFile().inStdlib()
 select r, "Import of child_process module in file \"" + r.getLocation().getFile().getBaseName().toString() + "\""