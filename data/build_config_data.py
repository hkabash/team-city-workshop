from pydantic import BaseModel, Field
from typing import List, Optional
from utils.data_generator import DataGenerator


class Property(BaseModel):
    name: str
    value: str


class StepProperties(BaseModel):
    property: List[Property]


class Step(BaseModel):
    name: str
    type: str = Field(..., alias='type')  # Используйте alias, если 'type' является зарезервированным словом в Python
    properties: StepProperties


class Steps(BaseModel):
    step: List[Step]


class Project(BaseModel):
    id: str


class BuildConfigModel(BaseModel):
    id:  Optional[str] = None
    name: str
    project: Project
    steps: Optional[Steps] = None


class BuildConfigRequiredFieldsOnlyModel(BaseModel):
    name: str
    project: Project


class BuildConfigData:
    @staticmethod
    def create_build_config_data(project_id: str) -> BuildConfigModel:
        # Создаем экземпляр Project
        project = Project(id=project_id)

        # Создаем список свойств для шага
        properties = [
            Property(name="script.content", value="echo 'Hello World!'"),
            Property(name="teamcity.step.mode", value="default"),
            Property(name="use.custom.script", value="true")
        ]

        # Создаем экземпляр Step с этими свойствами
        step = Step(name="myCommandLineStep", type="simpleRunner", properties=StepProperties(property=properties))

        # Создаем экземпляр Steps с этим шагом
        steps = Steps(step=[step])

        # Создаем и возвращаем экземпляр BuildConfigModel
        return BuildConfigModel(
            id=DataGenerator.fake_build_id(),
            name=DataGenerator.fake_name(),
            project=project,
            steps=steps
        )

    @staticmethod
    def create_build_config_data_with_required_fields_only(project_id: str) -> BuildConfigRequiredFieldsOnlyModel:
        # Создаем экземпляр Project
        project = Project(id=project_id)

        # Создаем и возвращаем экземпляр BuildConfigRequiredFieldsOnlyModel
        return BuildConfigRequiredFieldsOnlyModel(
            name=DataGenerator.fake_name(),
            project=project
        )


class Parameters(BaseModel):
    property: List = []
    count: int
    href: str


class ProjectResponse(BaseModel):
    id: str
    name: str
    parentProjectId: str
    href: str
    webUrl: str


class Templates(BaseModel):
    count: int
    buildType: List = []


class VcsRootEntries(BaseModel):
    count: int
    vcs_root_entry: List = []


class PropertiesResponse(BaseModel):
    property: List[Property]
    count: int


class StepResponse(BaseModel):
    id: str
    name: str
    type: str = Field(..., alias='type')  # Используйте alias, если 'type' является зарезервированным словом в Python
    properties: PropertiesResponse


class StepsResponse(BaseModel):
    step: Optional[List[StepResponse]] = None
    count: int


class BuildConfigResponseModel(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str
    project: ProjectResponse
    templates: Templates
    vcs_root_entries: VcsRootEntries = Field(..., alias='vcs-root-entries')
    settings: PropertiesResponse
    parameters: Parameters
    steps: StepsResponse
    features: dict
    triggers: dict
    snapshot_dependencies: dict = Field({}, alias='snapshot-dependencies')
    artifact_dependencies: dict = Field({}, alias='artifact-dependencies')
    agent_requirements: dict = Field({}, alias='agent-requirements')
    builds: dict
    investigations: dict
    compatibleAgents: dict
    compatibleCloudImages: dict
