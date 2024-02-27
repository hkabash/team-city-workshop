from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class BuildConfigAPI(CustomRequester):

    def create_build_config(self, build_config_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildTypes", data=build_config_data,
                                 expected_status=expected_status)

    def get_build_configs(self):
        return self.send_request("GET", "/app/rest/buildTypes")

    def get_build_config_by_locator(self, locator):
        return self.send_request("GET", f"/app/rest/buildTypes/{locator}")
