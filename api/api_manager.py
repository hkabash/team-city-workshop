from api.project_api import ProjectAPI
from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.build_config_api import BuildConfigAPI
from api.build_run_api import BuildRunAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.project_api = ProjectAPI(session)
        self.build_config_api = BuildConfigAPI(session)
        self.build_run_api = BuildRunAPI(session)

    def close_session(self):
        self.session.close()
