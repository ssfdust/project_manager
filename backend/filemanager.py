from backend.models import FrontendFileStatusModel, BackendFileStatusModel
from django.utils import timezone
from backend.confparse import CONFIG
import time
import datetime
from zipfile import ZipFile
from math import ceil
import shutil
import logging
import os
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
    @property
    def file_total(self):
        " return the total number of files"
        file_number = FrontendFileStatusModel.objects.count()

        return file_number


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
            # Verify input, uncompress the data into the variables
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

            # create a new file
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
    @property
    def file_total(self):
        " return the total number of files"
        file_number = FrontendFileStatusModel.objects.count()

        return file_number

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

def file_handler(kind, path, filename, action, page):
    """
    we use a dictionary object to handler the file
    action.It contains four kinds of operation.
    : active_action:if the target is existed and set the 
                    active flag to the database.
                    if the target is not existed, create
                    a row in the database and active it.
                    when receive a new file, this is the
                    default action for the new file.
    : get_action: get the filelist
    : delete_action: delete the file and data in database.

    the function will return a dictionary contains a two elements,
    one for "filelist", the other for "metadata".
    : return: a dictionary object.
    : filelist: a list of list which contains file info.
    : metadata: : page: the current page according to request.
                : total: the number of all the files.
                : all_pages: the total page number.

    """
    fileret = dict()
    def delete_action():
        top_file_info = file_status.get_filestatus(1)[0]
        if top_file_info[0] == filename and \
                top_file_info[2] == True:
                logger.warning('attemp to remove a file in use and failed')
                return False
        rel_f = os.path.join(path, filename)
        try:
            os.remove(rel_f)
        except FileNotFoundError:
            logger.error('file %s not found' % rel_f)
            return False
        except PermissionError:
            logger.error('you have no permission on that file')
            return False
        except:
            logger.error('unknown reason, cannot remove file %s' % rel_f)
            return False
        else:
            file_status.delete_filestatus(filename)
        return True

    def active_action():

        # clear the target directory and unzip the target file
        try:
            rel_f = os.path.join(path, filename)
            shutil.rmtree(CONFIG[kind]['workpath'])
            os.mkdir(CONFIG[kind]['workpath'])
            zip_in = ZipFile(rel_f)
            zip_in.extractall(path=CONFIG[kind]['workpath'])
            zip_in.close()
            logger.info('Now active frontend file, unzip file %s' % filename)
        except PermissionError:
            logger.error('Permission denied on creating file')
            return False
        except FileNotFoundError:
            if not os.path.exists(rel_f):
                logger.error('the zip file %s is not found' % rel_f)
            elif not os.path.exists(CONFIG[kind]['workpath']):
                logger.error('the workpath %s is not found' % CONFIG[kind]['workpath'] )
            return False
        except:
            logger.error('unknown error detected')
            return False
        else:
            # set the flag in the database
            now = timezone.localtime()
            _file_mt = time.localtime(os.stat(rel_f).st_mtime)
            file_mt = time.strftime('%Y-%m-%d %H:%M:%S', _file_mt)
            file_status.set_filestatus = (filename, file_mt, now, True)
        return True

    def get_action():
        file_list = file_status.get_filestatus(page)
        logger.debug('Get the active file, the file is %s' % file_list)
        return file_list
    if kind == 'frontend':
        logger.info('receive request for frontend')
        file_status = FrontendFileStatus()
    elif kind == 'backend':
        logger.info('receive request for backend')
        file_status = BackendFileStatus()
    else:
        logger.error('the file request not match anything')
        return None
    actions = {
        "delete": delete_action,
        "active": active_action
    }
    if action in actions: 
        actions[action]()
    # At last, we get the file status
    fileret['filelist'] = get_action()
    fileret['metadata'] = dict()
    fileret['metadata']['total'] = file_status.file_total
    fileret['metadata']['page'] = page if page else 1
    fileret['metadata']['all_page'] = ceil(file_status.file_total / 10)

    return fileret
