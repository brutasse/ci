from celery.decorators import task

from .exceptions import BuildException
from .models import Build, MetaBuild, Project


@task(ignore_result=True)
def execute_build(build_id):
    try:
        Build.objects.get(pk=build_id).execute()
    except BuildException:
        pass  # It's being reported, task is complete.


@task(ignore_result=True)
def execute_metabuild(metabuild_id):
    """
    Sequential build.
    """
    meta = MetaBuild.objects.get(pk=metabuild_id)
    for build in meta.builds.all():
        try:
            build.execute()
        except BuildException:
            pass


@task(ignore_result=True)
def clone_on_creation(project_id):
    Project.objects.get(pk=project_id).update_source()
