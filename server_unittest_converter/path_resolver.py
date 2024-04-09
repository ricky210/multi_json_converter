import os

from server_unittest_converter.config import Config
from server_unittest_converter.enums.case_type import CaseType


def get_output_dir( function_id: str, action_id: str, case_type: CaseType, test_case: str) -> str:
    """ 機能ID、アクションID、テストケースから出力ディレクトリを取得する """
    if case_type in [CaseType.REQ_REDIS, CaseType.RES_REDIS, CaseType.REQ_ACTION, CaseType.RES_ACTION, CaseType.REQ_DAO, CaseType.RES_DAO]:
        category = "API"
        return f"{Config.output_dir}/{function_id}_日本語機能名/{action_id}/{test_case}/{category}"

    elif case_type in [CaseType.DB_IN, CaseType.DB_OUT]:
        category = "DB"
        return f"{Config.output_dir}/{function_id}_日本語機能名/{action_id}/{test_case}/{category}"

    elif case_type == CaseType.API_STUB:
        category = "STUB"
        return f"{Config.output_dir}/{function_id}_日本語機能名/{action_id}/{test_case}/{category}"
    
    elif case_type == CaseType.VITEST_CONF:
        return f"{Config.output_dir}/{function_id}_日本語機能名/{action_id}"

    else:
        category = "OTHER(出力エラー)"
        return f"{Config.output_dir}/{function_id}_日本語機能名/{action_id}/{test_case}/{category}"
    
    return f"{Config.output_dir}/{function_id}_日本語機能名/{action_id}/{test_case}/{category}"


def get_output_file(case_type: CaseType, case_id: str, **kwargs) -> str:
    """ テストケース出力ファイル名を取得する
    Args:
        case_type (CaseType): テストケースの種類
        case_id (str): テストケースID
        table_name: テーブル名(DB_IN/DB_OUTで必須)
        framework_sid: フレームワークセッションID(Actionのリクエストで使用)、デフォルト=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        response_code: レスポンスコード(Actionのレスポンスで使用)、デフォルト=200
        stub_name: スタブ名(スタブで必須)
    """
    if case_type == CaseType.REQ_REDIS:
        return "01_request_redis.json"
    
    elif case_type == CaseType.RES_REDIS:
        return "unexpected_file.json"

    elif case_type == CaseType.REQ_ACTION:
        framework_sid:str = kwargs.get("framework_sid", "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
        return f"02_request_{case_id}_{framework_sid}.json"

    elif case_type == CaseType.RES_ACTION:
        status_code:str = kwargs.get("response_code", "200")
        return f"response_{case_id}_{status_code}.json"

    elif case_type == CaseType.REQ_DAO:
        framework_sid:str = kwargs.get("framework_sid", "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
        return f"01_request_postman_{case_id}_{framework_sid}.json"

    elif case_type == CaseType.RES_DAO:
        return f"response_{case_id}_200.json"

    elif case_type == CaseType.DB_IN:
        table_name:str = kwargs.get("table_name", "unexpected_table")
        return f"DB_IN_{table_name}.csv"

    elif case_type == CaseType.DB_OUT:
        table_name:str = kwargs.get("table_name", "unexpected_table")
        return f"DB_OUT_{table_name}.csv"

    elif case_type == CaseType.API_STUB:
        return f"stub_{stub_name}.json"
    
    elif case_type == CaseType.VITEST_CONF:
        return "config.yaml"

    else:
        return "unexpected_file.json"

def create_dir(dir_path: str) -> None:
    """ ディレクトリを作成する """
    os.makedirs(dir_path, exist_ok=True)