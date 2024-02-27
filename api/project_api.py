from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class ProjectAPI(CustomRequester):

    def create_project(self, project_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/projects", data=project_data,
                                 expected_status=expected_status)

    def get_projects(self):
        return self.send_request("GET", "/app/rest/projects")

    def delete_project(self, project_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/projects/id:{project_id}",
                                 expected_status=expected_status)

    def get_project_by_locator(self, locator, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/projects/{locator}",
                                 expected_status=expected_status)

    def clean_up_project(self, created_project_id):
        get_projects_response = self.get_projects().json()
        project_ids = [project.get('id', "") for project in get_projects_response.get('project', [])]
        if created_project_id in project_ids:
            self.delete_project(created_project_id)
            get_project_response = self.get_project_by_locator(created_project_id,
                                                               expected_status=HTTPStatus.NOT_FOUND).text
            assert f"No project found by name or internal/external id '{created_project_id}'." in get_project_response,\
                f"Project with '{created_project_id}' is still present in projects"
