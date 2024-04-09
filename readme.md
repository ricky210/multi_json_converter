# multi json converter(単体テスト用)の使い方

## 使い方
### Dockerを用いる方法
1. inputディレクトリに{機能ID}_TestData.xlsxファイルを配置する。
2. docker-compose.ymlファイルが配置されているディレクトリで下記commandを実行する。
(プログラムのバージョンアップ時には```--build```オプションを追加してください。)
```bash
docker compose up
```
3. outputディレクトリに出力された成果物をvitestに配置してテストを実行する。

### ローカルのpythonを用いる方法
**初回のみ**  
1. 必要なライブラリ(pandas, openpyxl)をインストールする。
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org  --trusted-host pypi.python.org pandas openpyxl
```

**テストケース生成時**
1. inputディレクトリに{機能ID}_TestData.xlsxファイルを配置する。
2. このreadme.mdが配置されているフォルダで下記commandを実行する。
```bash
python -m server_unittest_converter
```
3. outputディレクトリに出力された成果物をvitestに配置してテストを実行する。
