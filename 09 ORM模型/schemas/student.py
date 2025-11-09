from typing import List
from pydantic import BaseModel, field_validator

class StudentCreate(BaseModel):
    # id: int # 主键默认自增所有不需要写
    name: str
    pwd: str
    sno: int
    clas_id: int
    courses: List[int] = []

    @field_validator("sno")
    def sno_valid(cls, value):
        # 检查范围是否合法（2023001 到 2023999 之间）
        if not (2023000 < value < 2024000):
            raise ValueError("学生学号范围错误（应在 [2023001-2023999] 之间）")
        
        return value