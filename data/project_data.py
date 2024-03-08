from typing import Optional
from utils.data_generator import DataGenerator
from pydantic import BaseModel


class ParentProjectModel(BaseModel):
    id: str
    name: str
    description: str
    href: str
    webUrl: str


class BuildTypes(BaseModel):
    count: int
    buildType: list = []


class Templates(BaseModel):
    count: int
    buildType: list = []


class ParametersModel(BaseModel):
    property: list = []
    count: int
    href: str


class ProjectResponseModel(BaseModel):
    id: str
    name: str
    parentProjectId: str
    virtual: bool
    description: Optional[str] = None
    href: str
    webUrl: str
    parentProject: ParentProjectModel
    buildTypes: Optional[BuildTypes] = None
    templates: Optional[Templates] = None
    deploymentDashboards: Optional[dict[str, int]] = None
    parameters: Optional[ParametersModel] = None
    vcsRoots: dict
    projectFeatures: dict
    projects: dict

    class Config:
        extra = "allow"


class ProjectDataModel(BaseModel):
    parentProject: Optional[dict] = None
    name: str
    id: Optional[str] = None
    copyAllAssociatedSettings: Optional[bool] = None


class ProjectDataNameOnlyModel(BaseModel):
    name: str


class ProjectData:
    @staticmethod
    def create_project_data() -> ProjectDataModel:
        return ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_project_id(),
            copyAllAssociatedSettings=True
        )

    @staticmethod
    def create_project_data_name_only() -> ProjectDataNameOnlyModel:
        return ProjectDataNameOnlyModel(
            name=DataGenerator.fake_name()
        )
