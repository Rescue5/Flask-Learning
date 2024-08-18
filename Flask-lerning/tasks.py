from invoke import task


@task(default=True)
def frmt(c):
    """Автоформат под пеп8"""
    c.run("autopep8 -i *.py */*.py")


@task
def git(c):
    """Авто-пуш в гит в экстренных ситуациях"""
    c.run("git add .")
    c.run("git commit -m 'invoke commit'")
    c.run("git push")
