from __future__ import unicode_literals
import dateutil.parser
import requests

from api.models import Brigade, Project
from api.snapshots.cfa_snapshots import BrigadeSnapshot, ProjectSnapshot

CFA_ORGANIZATIONS_API_ENDPOINT = 'http://codeforamerica.org/api/organizations'
CFA_ORGANIZATIONS_PROJECTS_API_ENDPOINT = 'http://codeforamerica.org/api/organizations/{}/projects'

def scrape_brigades_and_projects():

    next_page = CFA_ORGANIZATIONS_API_ENDPOINT
    while next_page:
        try:
            page = requests.get(next_page).json()
        except ValueError, e:
            raise e  # maybe do error handling later, but for now let's just note this can throw ValueError

        if page.get('pages', None):
            next_page = page.get('pages').get('next', None)
        else:
            next_page = None

        objects = page.get('objects', list())
        for brigade in objects:
            brigade_object = Brigade.objects.filter(id=brigade.get('id')).first()
            if not brigade_object:
                brigade_object = Brigade(id=brigade.get('id'))
            brigade_object.name = brigade.get('name')
            brigade_object.city = brigade.get('city')
            brigade_object.latitude = brigade.get('latitude')
            brigade_object.longitude = brigade.get('longitude')
            brigade_object.started_on = brigade.get('started_on')
            brigade_object.website = brigade.get('website')
            brigade_object.type = brigade.get('type')
            brigade_object.events_url = brigade.get('events_url')
            brigade_object.rss = brigade.get('rss')
            brigade_object.save()
            BrigadeSnapshot().create_snapshot(brigade_object)

            scrape_projects_for_brigade(brigade_object)


def scrape_projects_for_brigade(brigade_object):
    next_page = CFA_ORGANIZATIONS_PROJECTS_API_ENDPOINT.format(brigade_object.id)
    while next_page:
        try:
            page = requests.get(next_page).json()
        except ValueError, e:
            raise e  # maybe do error handling later, but for now let's just note this can throw ValueError

        if page.get('pages', None):
            next_page = page.get('pages').get('next', None)
        else:
            next_page = None

        objects = page.get('objects', list())
        for project in objects:
            project_object = Project.objects.filter(id=project.get('id')).first()
            if not project_object:
                project_object = Project(id=project.get('id'))
            project_object.name = project.get('name')
            project_object.description = project.get('description')
            project_object.link_url = project.get('link_url')
            project_object.code_url = project.get('code_url')
            project_object.status = project.get('status')
            project_object.tags = project.get('tags')
            project_object.organization_name = project.get('organization_name')
            project_object.last_updated = dateutil.parser.parse(project.get('last_updated'))
            project_object.brigade_id = brigade_object.id
            project_object.save()
            ProjectSnapshot().create_snapshot(project_object)
