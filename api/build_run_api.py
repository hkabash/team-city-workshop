from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class BuildRunAPI(CustomRequester):

    def run_build_config(self, build_run_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildQueue", data=build_run_data,
                                 expected_status=expected_status)

    def get_build_status(self, build_config_id):
        return self.send_request("GET", f"/app/rest/buildQueue?locator=buildType(id:{build_config_id})")
