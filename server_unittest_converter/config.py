import argparse
import os
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

class Config:
    _simple_log_format: str = "[%(levelname)s] %(message)s"
    _detail_log_format: str = "[%(levelname)s] %(name)s %(funcName)s (line %(lineno)d): %(message)s"

    log_level: int = INFO
    output_dir: str = "./output"
    log_format: str = _simple_log_format

    @classmethod
    def load_args(cls) -> None:
        """ コマンドライン引数を読み込む(上書き) """

        # コマンドライン引数の定義
        parser = argparse.ArgumentParser(description="サーバ単体テストのエクセルデータをJSON/CSVに変換する")
        parser.add_argument("-o", "--output_dir", help="出力先ディレクトリ")
        parser.add_argument("-l", "--log_level", help="ログレベル(DEBUG, INFO, WARNING, ERROR, CRITICAL)", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        parser.add_argument("--log_format", help="ログのフォーマット", choices=["SIMPLE", "DETAIL"])

        # コマンドライン引数の解析
        args = parser.parse_args()
        log_level = args.log_level
        output_dir = args.output_dir
        log_format = args.log_format

        # コマンドライン引数が存在する場合、クラス変数に設定
        if (log_level is not None):
            Config.log_level = Config._parse_log_level(log_level)

        if (output_dir is not None):
            Config.output_dir = output_dir

        if (log_format is not None):
            if log_format == "SIMPLE":
                Config.log_format = Config._simple_log_format

            elif log_format == "DETAIL":
                Config.log_format = Config._detail_log_format

    @classmethod
    def load_env(cls) -> None:
        """ 環境変数を読み込む(上書き) """

        # 環境変数からログレベルを取得
        log_level_str = os.getenv("SUC_LOG_LEVEL")
        if log_level_str is not None:
            Config.log_level = Config._parse_log_level(log_level_str)

        # 環境変数から出力先ディレクトリを取得
        output_dir = os.getenv("SUC_OUTPUT_DIR")
        if output_dir is not None:
            Config.output_dir = output_dir

        # 環境変数からログのフォーマットを取得
        log_format = os.getenv("SUC_LOG_FORMAT")
        if log_format is not None:
            if log_format == "SIMPLE":
                Config.log_format = Config._simple_log_format

            elif log_format == "DETAIL":
                Config.log_format = Config._detail_log_format
                
    @classmethod
    def _parse_log_level(cls, log_level_str: str) -> int:
        """ ログレベルの文字列を、ログレベルの定数に変換する"""

        if log_level_str == "DEBUG":
            return DEBUG
        elif log_level_str == "INFO":
            return INFO
        elif log_level_str == "WARNING":
            return WARNING
        elif log_level_str == "ERROR":
            return ERROR
        elif log_level_str == "CRITICAL":
            return CRITICAL
        else:
            return INFO
