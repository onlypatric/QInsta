from dataclasses import dataclass
from enum import Enum

class TargetType(Enum):
  FOLLOWERS = "followers"
  FOLLOWINGS = "followings"
  HASHTAGS = "hashtags"
  LIKES = "likes"
  COMMENTS = "comments"
@dataclass()
class ExtractionParams:
  username:str
  password:str
  target:str
  target_type:TargetType
  max_amount:int
  output_path:str
  save_user_id:bool
  proxy:str