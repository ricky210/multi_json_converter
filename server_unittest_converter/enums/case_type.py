from __future__ import annotations
from enum import Enum, auto

class CaseType(Enum):
    REQ_REDIS = auto() # Redisリクエスト
    RES_REDIS = auto() # Redisレスポンス(未使用)
    REQ_ACTION = auto() # Actionリクエスト
    RES_ACTION = auto() # Actionレスポンス
    REQ_DAO = auto() # DAOリクエスト
    RES_DAO = auto() # DAOレスポンス
    DB_IN = auto() # DB投入データ
    DB_OUT = auto() # テスト後DB状態
    API_STUB = auto() # APIスタブ
    OTHERS = auto() # その他(エクセルのプルダウン設定用の「リスト」シートなどを想定)

    @classmethod
    def get_instance_from_sheet_name(cls, sheet_name: str) -> CaseType:
        if sheet_name.startswith("redis"):
            return CaseType.REQ_REDIS
        
        elif sheet_name.startswith("request_A") or sheet_name.startswith("request_X"):
            return CaseType.REQ_ACTION
        
        elif sheet_name.startswith("response_A") or sheet_name.startswith("response_X"):
            return CaseType.RES_ACTION
        
        elif sheet_name.startswith("request_SQL"):
            return CaseType.REQ_DAO
        
        elif sheet_name.startswith("response_SQL"):
            return CaseType.RES_DAO
        
        elif sheet_name.startswith("DBIN"):
            return CaseType.DB_IN
        
        elif sheet_name.startswith("DBOUT"):
            return CaseType.DB_OUT
        
        elif sheet_name.startswith("API") or sheet_name.startswith("FCT"):
            return CaseType.API_STUB
        
        else:
            return CaseType.OTHERS
