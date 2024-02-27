from pydantic import BaseModel, Field
from typing import List, Optional


class BuildType(BaseModel):
    id: str


class BuildConfigRunDataModel(BaseModel):
    buildType: BuildType


class BuildConfigRunData:
    @staticmethod
    def create_build_run_data(build_config_id) -> BuildConfigRunDataModel:
        build_type = BuildType(id=build_config_id)
        return BuildConfigRunDataModel(
            buildType=build_type
        )


class User(BaseModel):
    username: str
    name: str
    id: int
    href: str


class Triggered(BaseModel):
    type: str
    date: str
    user: User


class BuildTypeResponse(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str


class Changes(BaseModel):
    href: str


class CompatibleAgents(BaseModel):
    href: str


class Artifacts(BaseModel):
    href: str


class BuildRunResponseModel(BaseModel):
    id: int
    buildTypeId: str
    state: str
    href: str
    webUrl: str
    buildType: BuildTypeResponse
    waitReason: Optional[str] = None
    queuedDate: str
    triggered: Triggered
    changes: Changes
    revisions: dict = Field(default_factory=dict)
    compatibleAgents: CompatibleAgents
    artifacts: Artifacts
    vcsLabels: List = Field(default_factory=list)
    customization: dict = Field(default_factory=dict)


class BuildQueueResponse(BaseModel):
    count: int
    href: str
    build: List = []
