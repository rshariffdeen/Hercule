project('poc', 'python', 'java')

python_dep = dependency('python3')

python_sources = files(
    'poc/poc.py',
    # Include other Python source files if any
)

java_sources = files(
    'poc/java/*.java',
    # Include other Java source files if any
)

jar_target = jar('helper.jar', sources: java_sources)

executable('poc', python_sources, jar_target, dependencies: python_dep)
