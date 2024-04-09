import glob
import openpyxl
import os
from logging import getLogger, StreamHandler, Formatter

from server_unittest_converter import converter, vitest_config
from server_unittest_converter.config import Config

def getExcelFileList(dir: str) -> list[str]:
    """ 指定されたフォルダ内の、エクセルファイルの一覧を取得する"""
    candidates = glob.glob(f"{dir}/*.xlsx") + glob.glob(f"{dir}/*.xls") + glob.glob(f"{dir}/*.xlsm")
 
    return [file for file in candidates if not os.path.basename(file).startswith("~$")]


def main():
    """ メイン処理 """

    # 環境変数の読み込み
    Config.load_env()

    # 引数の読み込み
    Config.load_args()
    
    # ロガー(全体)の設定
    root_logger = getLogger(__package__)
    log_level = Config.log_level
    root_logger.setLevel(log_level)

    # ストリームハンドラーの設定
    stream_handler = StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(Formatter(Config.log_format))
    root_logger.addHandler(stream_handler)

    # ロガー(メイン処理)の設定
    logger = root_logger.getChild(__name__)

    # エクセルファイル一覧の取得
    input_file_names = getExcelFileList("./input")
    logger.info(f"処理対象ファイル一覧: {input_file_names}")

    # 各エクセルファイルに対して処理を実行
    for input_file_name in input_file_names:
        logger.info(f"処理開始(ファイル): {input_file_name}")

        # 各シートに対して処理を実行
        workbook = openpyxl.load_workbook(input_file_name, data_only=True)
        sheet_names = workbook.sheetnames
        logger.debug(f"  シート一覧: {sheet_names}")

        for sheet_name in sheet_names:
            logger.info(f"  処理開始(シート): {sheet_name}")

            # シートからテスト用JSON/CSVファイルを生成
            converter.convert_excel_to_testfiles(input_file_name, sheet_name)
            
            logger.info(f"  処理終了(シート): {sheet_name}")

         # コンフィグファイルを生成
        vitest_config.create_config_files(input_file_name, sheet_names)
        
        logger.info(f"処理終了(ファイル): {input_file_name}")


    logger.info("FINISHED")

if __name__ == '__main__':
    main()
