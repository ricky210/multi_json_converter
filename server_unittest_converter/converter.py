import json
import openpyxl
import os
import pandas as pd
import re
import traceback
from logging import getLogger
 
from server_unittest_converter import path_resolver, tanba, util
from server_unittest_converter.enums.case_type import CaseType
 
# ロガー
logger = getLogger(__package__).getChild(__name__)
 
 
def convert_excel_to_testfiles(input_file_name:str) -> None:
    """ エクセルファイルを読み込み、テスト用ファイルに変換する """
    # 各シートに対して処理を実行
    workbook = openpyxl.load_workbook(input_file_name, data_only=True)
    sheet_names = workbook.sheetnames
    logger.debug(f"  シート一覧: {sheet_names}")

    for sheet_name in sheet_names:
        logger.info(f"  処理開始(シート): {sheet_name}")

        # シート名からケースタイプを取得
        case_type: CaseType = CaseType.get_instance_from_sheet_name(sheet_name)
        logger.debug(f"    シート名: {sheet_name}, ケースタイプ: {case_type}")

        # ケースタイプに応じた処理を実行
        if (case_type in [CaseType.REQ_REDIS, CaseType.RES_REDIS, CaseType.REQ_ACTION, CaseType.RES_ACTION, CaseType.REQ_DAO, CaseType.RES_DAO, CaseType.API_STUB]):
            _convert_to_json_file(input_file_name, sheet_name, case_type)

        elif (case_type in [CaseType.DB_IN, CaseType.DB_OUT]):
            _convert_to_db_file(input_file_name, sheet_name, case_type)

        else:
            logger.debug("    変換対象外のタイプのためスキップ")
        
        logger.info(f"  処理終了(シート): {sheet_name}")

 
def _convert_to_json_file(input_file_name: str, sheet_name: str, case_type: CaseType) -> None:
    """ エクセルファイルからJSONファイルに変換する """
    logger.debug("    JSON変換処理を開始")

    # 機能IDを取得
    function_id = util.get_function_id_from_file_name(input_file_name)
 
    # アクションID/SQLIDを取得
    action_id = util.get_action_id_from_sheet_name(sheet_name)
    logger.debug(f"    アクションID: {action_id}")
 
    # エクセルシートを読み込み
    sheet = pd.read_excel(
        input_file_name,
        sheet_name=sheet_name,
        dtype=str,
        engine="openpyxl"
    )
 
    # キーの一覧を取得
    keys = sheet.loc[:, 'Key']
 
    # テストケースの一覧を取得
    test_case_names = [col for col in sheet.columns if re.match(r"A|(SQL)[0-9]", col)]

    # 各テストケースごとの処理
    for test_case_name in test_case_names:
        logger.debug(f"      テストケース: {test_case_name}")
 
        # テストケースのデータを取得する
        test_case = sheet[test_case_name]
 
        # 1行目のデータを特別扱い(フレームワークセッションID または ステータスコード)
        framework_session_id = None
        status_code = None
        is_json = None
        inner_keys = keys

        if case_type in [CaseType.REQ_ACTION, CaseType.REQ_DAO] and keys[0] == "frameworkSessionId":
            framework_session_id = test_case[0]
 
        elif case_type == CaseType.RES_ACTION and keys[0] == "StatusCode":
            status_code = test_case[0]

        elif case_type == CaseType.RES_DAO and keys[0] == "IsJson":
            is_json = test_case[0]

        inner_keys = keys.drop([0])
        test_case.drop([0], inplace=True)
        inner_keys.reset_index(drop=True, inplace=True)
        test_case.reset_index(drop=True, inplace=True)


        # 特殊文字の置き換え
        test_case.fillna("", inplace=True)
        test_case = test_case.apply(_replace_special_characters_json)

        # テストケースがJSON形式ではない場合のみ特別扱い(DB_OUTのケース)
        if is_json == "$FALSE":
            output_dir_name = path_resolver.get_output_dir(function_id, action_id, case_type, test_case_name)
            output_file_name = path_resolver.get_output_file(case_type, test_case_name)
            output_path = f"{output_dir_name}/{output_file_name}"
            logger.debug(f"        出力先: {output_dir_name}, 出力ファイル名: {output_file_name}")

            logger.debug(f"        ファイル出力: {test_case[0]}")

            # ファイルを出力
            path_resolver.create_dir(output_dir_name)
            with open (output_path, "w") as f:
                f.write(test_case[0])

            continue

        # テストケースのデータを辞書に変換
        result_dic = {}
        for index, key in enumerate(inner_keys):
            value = test_case.iloc[index]
            try:
                tanba.nested_set(result_dic, key, value)
            except TypeError as e:
                # エラーが発生した場合、ログを出力して対象ケースのファイル出力を中断
                logger.warning(f"        階層構造が誤っています。対象ケースの一部は出力されません。 テストケース: {test_case_name}, key: {key}, value: {value}")
                logger.debug(f"        error: {traceback.extract_tb(e.__traceback__)}")
                return

        logger.debug(f"        JSON出力: {result_dic}")

        # 出力先パスと出力ファイル名を取得
        output_dir_name = path_resolver.get_output_dir(function_id, action_id, case_type, test_case_name)
        output_file_name = path_resolver.get_output_file(case_type, test_case_name, framework_sid=framework_session_id, response_code=status_code)
        output_path = f"{output_dir_name}/{output_file_name}"
        logger.debug(f"        出力先: {output_dir_name}, 出力ファイル名: {output_file_name}")

        # ファイルを出力
        path_resolver.create_dir(output_dir_name)
        with open(output_path, "w") as f:
            f.write(json.dumps(result_dic, indent=2, ensure_ascii=False))
        
        
    logger.debug("    JSON変換処理を終了")
 
def _replace_special_characters_json(value) -> str:
    """ 特殊文字を置き換える """
    if value == "$NULL":
        return None

    if value == "$SPACE":
        return " "

    if value == "$TRUE":
        return True

    if value == "$FALSE":
        return False
 
    return value

def _convert_to_db_file(input_file_name: str, sheet_name: str, case_type: CaseType) -> None:
    """ エクセルファイルからCSVファイルに変換する """
    logger.debug("    DB変換処理を開始")

    # 機能IDを取得
    function_id = util.get_function_id_from_file_name(input_file_name)

    # アクションID/SQLIDを取得
    action_id = util.get_action_id_from_sheet_name(sheet_name)
    logger.debug(f"    アクションID: {action_id}")
 
    # エクセルシートを読み込み
    sheet = pd.read_excel(
        input_file_name,
        sheet_name=sheet_name,
        dtype=str,
        header=None,
        engine="openpyxl"
    )

    # 空白行をキーにテーブルを分割して各テーブルをCSVファイルに変換
    line_a = sheet[0]
    row_from = None

    for idx, value in enumerate(line_a):
        if row_from == None and not pd.isna(value):
            row_from = idx

        elif row_from != None and pd.isna(value):
            row_to = idx
            table = sheet[row_from:row_to]
            table.dropna(how="all", axis=1, inplace=True)
            table.reset_index(drop=True, inplace=True)
            _convert_table_to_csv_file(table, case_type, function_id, action_id)
            row_from = None

        elif row_from != None and idx == len(line_a) - 1:
            row_to = idx + 1
            table = sheet[row_from:row_to]
            table.dropna(how="all", axis=1, inplace=True)
            table.reset_index(drop=True, inplace=True)
            _convert_table_to_csv_file(table, case_type, function_id, action_id)
 
    logger.debug("    DB変換処理を終了")

def _convert_table_to_csv_file(table: pd.DataFrame, case_type: CaseType, function_id: str, action_id: str) -> None:
    """ テーブルをCSVファイルに変換する"""
    # スキーマ名.テーブル名を取得
    table_name = table[0][0]

    # データ本体が記述された範囲にテーブルを絞る
    inner_table = table.iloc[2:]
    inner_table.columns = table.iloc[1]

    # テストケース一覧を取得
    test_cases = [val for val in list(set(inner_table.iloc[:, 0])) if val != "$MASTER" and not pd.isna(val)]

    # $EMPTYの行を削除
    inner_table = inner_table.drop(inner_table[inner_table.iloc[:, 2] == "$EMPTY"].index)

    # テーブルを各テストケースごとに絞る
    for test_case in test_cases:
        # 0列目がテストケース名/$MASTERの行を取得
        data_table = inner_table[(inner_table.iloc[:, 0] == test_case) | (inner_table.iloc[:, 0] == "$MASTER")]
        
        # 左2列を削除
        output_table = data_table.iloc[:, 2:]

        # 出力先パスと出力ファイル名を取得
        output_dir_name = path_resolver.get_output_dir(function_id, action_id, case_type, test_case)
        output_file_name = path_resolver.get_output_file(case_type, test_case, table_name=table_name)
        output_path = f"{output_dir_name}/{output_file_name}"
        logger.debug(f"        出力先: {output_dir_name}, 出力ファイル名: {output_file_name}")

        # ファイルを出力
        path_resolver.create_dir(output_dir_name)
        output_table.to_csv(output_path, index=False, header=True)
