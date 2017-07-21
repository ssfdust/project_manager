import os
from backend.models import FrontendFileStatusModel, BackendFileStatusModel
from django.utils import timezone
import time
import datetime
import logging
import pytz

logger = logging.getLogger('django')
class FrontendFileStatus(object):
    """
    The class is for easy database accessing.
    It is based on the FrontendFileStatusModel model.
    This model contains four columns.
    :filename: the flie name
    :modified_date: the modified time of the file, which should be 
                        kept with the system file modified time.So
                        this field should be checked or updated for
                        every access.
    :enabled_date: if this file has been enabled, update the field
                        with the timezone.now function.
    :in_use:       similar updated way along with the enabled_date 
    """

    def get_filestatus(self, page):
        """
        the get_filestatus function accept two
        arguments, one for self, the ohter for
        page.
        We use Entry.objects.all()[:] slice structure 
        to get the listed file.It applies the action
        with the SQL's LIMIT and OFFSET claues.

        This function accept one argument.
        : page: the number of the page to be shown

        : return: the list of file info contains four
                fields mentioned above.
                e.g
                [
                    ['filename1', '2003-09-23 04:23:25', '2003-09-25 09:24:24', True],
                    ['filename2', '2003-09-24 04:23:25', '2003-09-26 09:24:24', False],
                    ['filename3', '2003-09-25 04:23:25', '2003-09-27 09:24:24', False],
                ]
        """
        file_list = list()

        file_number = FrontendFileStatusModel.objects.count()
        start = (page - 1) * 10
        end = start + 10
        if start > file_number:
            logger.error('the request page is not existed')
            return []

        # Cache the query to avoid repeated evaluating query
        # reference: https://docs.djangoproject.com/el/1.10/topics/db/queries/#caching-and-querysets

        # Not cached here
        query_set = FrontendFileStatusModel.objects.all().order_by('-enabled_date')[start:end]
        for query in query_set:
            # The query has been cached
            file_list.append(query.file_info)

        # sort the file_list
        file_list.sort(key=lambda x:x[1], reverse=True)
        file_list.sort(key=lambda x:x[3], reverse=True)
        self._file = file_list
        return self._file

    def delete_filestatus(self, filename):
        """
        :filename: the file name to delete
        :return: success if the file exists, otherwise
                return False
        """
        file_q = FrontendFileStatusModel.objects.filter(filename=filename)
        if file_q.exists():
            file_to_delete = file_q.get()
            file_to_delete.delete()
            return True
        else:
            return False

    @property
    def set_filestatus(self):
        pass
    
    @set_filestatus.setter
    def set_filestatus(self, file_status):
        try:
            # Verify input
            filename, modified_date, enabled_date, in_use = file_status
        except ValueError:
            raise ValueError('Pass an iterable with two items')
        else:
            # get old file in use and stop it
            file_in_use_q = FrontendFileStatusModel.objects.filter(in_use=True)
            if file_in_use_q.exists() and in_use == True:
                file_in_use = file_in_use_q.get()
                logger.info('disable the old file in use')
                file_in_use.in_use = False
                file_in_use.save()
            elif not file_in_use_q.exists():
                logger.info('no frontend file enabled')

            new_file, created = FrontendFileStatusModel.objects.get_or_create(filename=filename)
            now = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
            new_file.modified_date = modified_date
            new_file.in_use = in_use
            if created and enabled_date != '':
                logger.info('A new file registed')
                new_file.enabled_date = enabled_date
            elif created and enabled_date == '':
                logger.warning('the enabled date field is empty, set it with modified date')
                new_file.enabled_date = modified_date
                logger.info(new_file.enabled_date)
            if in_use == True:
                logger.info('set new file in use')
                new_file.enabled_date = now
                logger.debug(now)
            new_file.save()

class BackendFileStatus(object):
    """
    The class is for easy database accessing.
    It is based on the BackendFileStatusModel model.
    This model contains four columns.
    :filename: the flie name
    :modified_date: the modified time of the file, which should be 
                        kept with the system file modified time.So
                        this field should be checked or updated for
                        every access.
    :enabled_date: if this file has been enabled, update the field
                        with the timezone.now function.
    :in_use:       similar updated way along with the enabled_date 
    """

    def get_filestatus(self, page):
        """
        the get_filestatus function accept two
        arguments, one for self, the ohter for
        page.
        We use Entry.objects.all()[:] slice structure 
        to get the listed file.It applies the action
        with the SQL's LIMIT and OFFSET claues.

        This function accept one argument.
        : page: the number of the page to be shown

        : return: the list of file info contains four
                fields mentioned above.
                e.g
                [
                    ['filename1', '2003-09-23 04:23:25', '2003-09-25 09:24:24', True],
                    ['filename2', '2003-09-24 04:23:25', '2003-09-26 09:24:24', False],
                    ['filename3', '2003-09-25 04:23:25', '2003-09-27 09:24:24', False],
                ]
        """
        file_list = list()

        file_number = BackendFileStatusModel.objects.count()
        start = (page - 1) * 10
        end = start + 10
        if start > file_number:
            logger.error('the request page is not existed')
            return []

        # Cache the query to avoid repeated evaluating query
        # reference: https://docs.djangoproject.com/el/1.10/topics/db/queries/#caching-and-querysets

        # Not cached here
        query_set = BackendFileStatusModel.objects.all().order_by('-enabled_date')[start:end]
        for query in query_set:
            # The query has been cached
            file_list.append(query.file_info)

        # sort the file_list
        file_list.sort(key=lambda x:x[1], reverse=True)
        file_list.sort(key=lambda x:x[3], reverse=True)
        self._file = file_list
        return self._file

    def delete_filestatus(self, filename):
        """
        :filename: the file name to delete
        :return: success if the file exists, otherwise
                return False
        """
        file_q = BackendFileStatusModel.objects.filter(filename=filename)
        if file_q.exists():
            file_to_delete = file_q.get()
            file_to_delete.delete()
            return True
        else:
            return False

    @property
    def set_filestatus(self):
        pass
    
    @set_filestatus.setter
    def set_filestatus(self, file_status):
        try:
            # Verify input
            filename, modified_date, enabled_date, in_use = file_status
        except ValueError:
            raise ValueError('Pass an iterable with two items')
        else:
            # get old file in use and stop it
            file_in_use_q = BackendFileStatusModel.objects.filter(in_use=True)
            if file_in_use_q.exists() and in_use == True:
                file_in_use = file_in_use_q.get()
                logger.info('disable the old file in use')
                file_in_use.in_use = False
                file_in_use.save()
            elif not file_in_use_q.exists():
                logger.info('no frontend file enabled')

            new_file, created = BackendFileStatusModel.objects.get_or_create(filename=filename)
            now = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
            new_file.modified_date = modified_date
            new_file.in_use = in_use
            if created and enabled_date != '':
                logger.info('A new file registed')
                new_file.enabled_date = enabled_date
            elif created and enabled_date == '':
                logger.warning('the enabled date field is empty, set it with modified date')
                new_file.enabled_date = modified_date
                logger.info(new_file.enabled_date)
            if in_use == True:
                logger.info('set new file in use')
                new_file.enabled_date = now
                logger.debug(now)
            new_file.save()

def frontend_file_handler(path, filename, action, page=None):
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
    frontend_fs = FrontendFileStatus()
    fileret = dict()
    filelist = list()
    def delete_action(filename, path):
        pass
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
