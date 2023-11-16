from pydantic import BaseModel


class TestScript(BaseModel):
    name: str
    commit_message: str 
    content: str
    branch: str
    repo_url: str
