import os
import sys
import logging
from datetime import datetime
from harvest.auth import PersonalAccessAuthClient
from harvest.api import Projects
from harvest.api import Tasks
from harvest.api import TimeEntry
from harvest.services import AllProjects
from harvest.services import AllTasks
try:
    from ConfigParser import ConfigParser
except ModuleNotFoundError as ex:
    from configparser import ConfigParser


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    client = PersonalAccessAuthClient(
        # cfg='.harvest.cfg'
    )
    cfg = os.environ.get(
        'HARVEST_CFG',
        os.path.expanduser('~/.harvest.cfg'),
    )
    config = ConfigParser()
    config.read(cfg)
    if sys.argv[1] == 'projects':
        api = Projects(client)
        if sys.argv[2] == 'get':
            if sys.argv[3] == 'all':
                # logging.info(api.get().json())
                for entity in AllProjects(cfg='harvest.cfg').all():
                    logging.info('{} - #{}'.format(
                        entity['name'], entity['id']))
    elif sys.argv[1] == 'tasks':
        api = Tasks(client)
        if sys.argv[2] == 'get':
            if sys.argv[3] == 'all':
                for entity in AllTasks(cfg='harvest.cfg').all():
                    logging.info('{} - #{}'.format(
                        entity['name'], entity['id']))
    elif sys.argv[1] == 'timeentry':
        api = TimeEntry(client)
        if sys.argv[2] == 'new':
            NOTES_ARG = 3
            SPENTDATE_ARG = 4
            TASKID_ARG = 5
            PROJECTID_ARG = 6
            HOURS = 7
            notes = sys.argv[NOTES_ARG]
            spent_date = sys.argv[SPENTDATE_ARG]
            if spent_date == 'today':
                spent_date = datetime.now().strftime('%Y-%m-%d')

            task_id = sys.argv[TASKID_ARG]
            if not task_id.isnumeric():
                task_id = config.get('tasks', task_id)

            if not sys.argv[PROJECTID_ARG]:
                logging.info('Missing project(s) ID list')
            project_id_list = []
            for entry in sys.argv[PROJECTID_ARG].split(','):
                if entry.isnumeric():
                    project_id_list.append(entry)
                else:
                    project_id_list.append(config.get('projects', entry))
            try:
                hours = sys.argv[HOURS]
            except IndexError:
                hours = 0.00
            for project_id in project_id_list:
                data = {
                    'notes': notes,
                    'spent_date': spent_date,
                    'task_id': task_id,
                    'project_id': project_id,
                    'hours': hours,
                }
                TimeEntry(client).post(data=data)