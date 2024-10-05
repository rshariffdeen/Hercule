/**
 * @name Detects system command executions with an encrypted payload
 * @description Detects a comand execution which passes an encrypted payload
 * @author Martin Mirchev
 * @kind problem
 * @problem.severity warning
 * @id py/system-command-execution-encrypted
 * @security-severity 2.0
 * @example-packages kraken-api
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs
import semmle.python.Concepts

from StrConst c
where
// Searches for a string that contains a base64 encoded payload which will be used by powershell
  c.getText().indexOf("powershell") > -1 and
  c.getText().regexpMatch(".*-[Ee^]{1,2}[NnCcOoDdEeMmAa^]+ [A-Za-z0-9+/=]{5,}.*")
  or
  c.getText().regexpMatch("[A-Za-z0-9+/=]{5,}.*") and
  c.getText().indexOf("base64 --decode") > -1 and
  c.getText().indexOf("bash") > -1
  // Searches for a string that contains a base64 encoded payload which will be used by unix base64 decode

select c,
  "Detected variation of encoded command " + c.getLocation() + " with value " +
    c.getText()
//from SystemCommandExecution execution
//select execution, "Detected SystemCommandExecution (" + execution.asExpr().(FunctionExpr).getName() + ")"
