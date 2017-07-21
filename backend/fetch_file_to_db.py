from django.db import migrations
from backend.confparse import get_config
import time
import os

def forwards_func(apps, schema_editor):
    """
    We need to list all the files and
    store the file status from the file
    to the database with the following
    options
    
    for the first time, we assume the create time
    as the enabled time.
    
    we verify whether a file exists via database
    get_or_create function.
    if the database column exists, we know the file
    has been added before.otherwise, we will verify the
    modified time of the file to update the modified time.
    If the column is not existed, we will add the column
    with the modified time as the enabled time.
    """
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    frontend_list = list()
    backend_list = list()
    frontend_path = get_config()['frontend']
    backend_path = get_config()['backend']
    FrontendFileStatusModel = apps.get_model("backend", "FrontendFileStatusModel")
    BackendFileStatusModel = apps.get_model("backend", "BackendFileStatusModel")

    for filename in os.listdir(frontend_path):
        rel_f_path = os.path.join(frontend_path, f)
        file_mt = get_file_mtime(rel_f_path)
        frontend_list.append(FrontendFileStatusModel(
            filename=filename,
            modified_date=file_mt,
            enabled_date='',
            in_use=False
        ))

    for filename in os.listdir(backend_path):
        rel_f_path = os.path.join(backend_path, f)
        file_mt = get_file_mtime(rel_f_path)
        backend_list.append(BackendFileStatusModel(
            filename=filename,
            modified_date=file_mt,
            enabled_date='',
            in_use=False
        ))

    db_alias = schema_editor.connection.alias

    FrontendFileStatusModel.objects.using(db_alias).bulk_create(frontend_list)
    BackendFileStatusModel.objects.using(db_alias).bulk_create(backend_list)

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    FrontendFileStatusModel = apps.get_model("backend", "FrontendFileStatusModel")
    BackendFileStatusModel = apps.get_model("backend", "BackendFileStatusModel")
    db_alias = schema_editor.connection.alias
    FrontendFileStatusModel.objects.using(db_alias).all().delete()
    BackendFileStatusModel.objects.using(db_alias).all().delete()


def get_file_mtime(filename):
    _file_mt = time.localtime(os.stat(filename).st_mtime)
    file_mt = time.strftime('%Y-%m-%d %H-%M-%d', _file_mt)
    return file_mt


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
