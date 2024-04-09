import os
from logging import getLogger

from server_unittest_converter import path_resolver, util
from server_unittest_converter.config import Config
from server_unittest_converter.enums.case_type import CaseType

# ロガー
logger = getLogger(__package__).getChild(__name__)

def create_config_files(input_file_name: str, sheet_names: list[str]):
    """ シートのリストからconfigファイルを生成する """
    logger.debug("    configファイル生成処理を開始")

    # 各シートごとに処理を実行
    for sheet_name in sheet_names:
        logger.debug(f"      シート名: {sheet_name}")

        # シート名からケースタイプを取得
        case_type: CaseType = CaseType.get_instance_from_sheet_name(sheet_name)
        logger.debug(f"    シート名: {sheet_name}, ケースタイプ: {case_type}")

        if case_type not in [CaseType.REQ_ACTION, CaseType.RES_ACTION]:
            logger.debug("    Config出力対象外のためスキップ")
            continue

        # 機能IDを取得
        function_id = util.get_function_id_from_file_name(input_file_name)

        # アクションID/SQLIDを取得
        action_id = util.get_action_id_from_sheet_name(sheet_name)
        logger.debug(f"      アクションID: {action_id}")

        # 出力先ディレクトリを取得
        output_dir = path_resolver.get_output_dir(function_id, action_id, CaseType.VITEST_CONF, None)
        output_file_name = path_resolver.get_output_file(CaseType.VITEST_CONF, None)
        output_path = f"{output_dir}/{output_file_name}"

        # 出力先ディレクトリの作成
        path_resolver.create_dir(output_dir)

        # configファイルを出力
        # TODO: path_resolverの対象にする
        if case_type == CaseType.REQ_ACTION:
            with open(output_path, "w") as f:
                f.writelines([
                    "api:\n",
                    "  02_request:\n"
                    f"    url: {{url}}"
                ])
