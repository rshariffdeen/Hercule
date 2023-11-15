/**
 * @name Detects IP addresses
 * @description Detects IP addresses as StringLiteral using a regular expression
 * @author Fabian Froh
 * @kind problem
 * @id js/ip-address
 * @security-severity 7.0
 * @problem.severity warning
 * @example-packages kraken-api
 * @tags security
 * ip address
 */

 import python
 import semmle.python.dataflow.new.TaintTracking
 import semmle.python.ApiGraphs
 

 from StringValue s
 where s.getText().regexpMatch(".*(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).*")
 // Do not match "safe" loopback address
 and not s.toString().matches(["%127.0.0.1%"])
 select s, "Detected the following IP address: " + s.toString()