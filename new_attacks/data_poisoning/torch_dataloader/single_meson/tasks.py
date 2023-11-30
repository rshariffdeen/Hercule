from invoke import task

@task
def build(ctx):
    ctx.run('meson build')
    ctx.run('ninja -C build')

@task
def install(ctx):
    ctx.run('ninja -C build install')

@task
def run_jar(ctx):
    ctx.run('java -jar helper.jar data.txt')
