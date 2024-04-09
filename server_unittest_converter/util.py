def get_function_id_from_file_name(file_name: str) -> str:
    """ ファイル名から機能IDを取得する """
    # _で分割する
    inner_file_name = os.path.basename(file_name)
    parts = inner_file_name.split("_")
 
    # 1番目の要素を返す
    if len(parts) >= 2:
        return parts[0]
 
    # 変換にした場合、SUBxxxを返す
    return "SUBxxx"
 
def get_action_id_from_sheet_name(sheet_name: str) -> str:
    """ シート名からアクションID/SQLIDを取得する """
    # _で分割する
    parts = sheet_name.split("_", 1)
 
    # 2番目の要素を返す
    if len(parts) == 2:
        return parts[1]
 
    return None