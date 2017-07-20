import os
from backend.models import FrontendFileStatusModel
import time
import logging

logger = logging.getLogger('django')
class FrontendFileStatus(object):
    @property
    def filestatus(self):
        fileobj_in_use = dict()
        try:
            filemod_in_use = FrontendFileStatusModel.objects.get(in_use=True)
            fileobj_in_use['filename'] = filemod_in_use.filename
            fileobj_in_use['create_date'] = filemod_in_use.create_date
        except:
            logger.info('no frontend file enabled')
            fileobj_in_use['filename'] = None
            fileobj_in_use['create_date'] = None
        self._file = fileobj_in_use
        return self._file

    @filestatus.setter
    def filestatus(self, file_status):
        try:
            filename, in_use = file_status
        except ValueError:
            raise ValueError('Pass an iterable with two items')
        else:
            file_in_use = dict()
            try:
                fileobj_in_use, created = FrontendFileStatusModel.objects.get_or_create(in_use=True)
                fileobj_in_use.in_use = False
                fileobj_in_use.save()
            except:
                if created == True:
                    fileobj_in_use.delete()
                logger.info('no frontend file enabled')
            finally:
                new_fileobj, created = FrontendFileStatusModel.objects.get_or_create(filename=filename, in_use=False)
                new_fileobj.in_use = in_use
                new_fileobj.save()

def frontend_file_handler(path, filename, action):
    frontend_fs = FrontendFileStatus()
    fileret = dict()
    filelist = list()
    def stop_action(filename, path):
        fileobj = dict()
        file_st = frontend_fs.filestatus

        if not file_st['filename']:
            logger.warning('No frontend file enabled, so nothing to do here')
            return False
        #TODO clear directory
        logger.info('Now empty the frontend directory for file %s' % filename)
        frontend_fs.filestatus = (filename, False)
        return True

    def active_action(filename, path):
        fileobj = dict()
        file_st = frontend_fs.filestatus
        #TODO clear the target directory and unzip the target file
        logger.info('Now active frontend file, unzip file %s' % filename)
        frontend_fs.filestatus = (filename, True)
        return True

    def get_action(filename, path):
        file_st = frontend_fs.filestatus 
        logger.info('Get the active file, the file is %s' % file_st['filename'])
        return file_st

    functions = {
        'get': get_action,
        'active':active_action,
        'stop': stop_action
    }
    func = functions[action]
    ret = func(filename, path)
    active_filename = frontend_fs.filestatus['filename']
    logger.info(active_filename)
    if ret == False:
        logger.warning('file action failed')
        return None
    for f in os.listdir(path):
        active = False
        rel_f = os.path.join(path, f)
        #get the create time
        _file_mt = time.localtime(os.stat(rel_f).st_mtime)
        file_mt = time.strftime('%Y-%m-%d %H-%M-%d', _file_mt)
        if f == active_filename:
            active = True
        filelist.append([f, file_mt, active])
    filelist.sort(key=lambda x:x[2], reverse=True)
    fileret['files'] = filelist
    fileret['metadata'] = {'file_num':len(os.listdir(path))}
    
    return fileret
