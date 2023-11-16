/**
 * @name Simple index usage of os.environ
 * @description Checking the local environment is suspicious
 * @kind problem
 * @problem.severity warning
 * @security-severity 7.8
 * @precision high
 * @id py/environ-simple-index
 * @tags security
 */

import python
import semmle.python.dataflow.new.TaintTracking
import semmle.python.ApiGraphs

from DataFlow::AttrRead read, DataFlow::Node p, string key
where
  read.accesses(API::moduleImport("os").getMember("environ").asSource(), key) and
  TaintTracking::localTaint(read.getALocalSource(), p)
select read.getLocation(),
  "Found a simple indexation read of the field " + key + " from os.environ , which flows to " +
    p.getLocation()
