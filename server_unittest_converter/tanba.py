from re import match

def _parse_key(key):
    parts = key.split('.')
    return [int(p) if p.isdigit() else p for p in parts]

def nested_set(dic, key, value):
    keys = _parse_key(key)
        
    # $EMPTYが入っている場合、空のリストとする
    if value == "$EMPTY":
        dic[keys[0]] = []
        return
    for key in keys[:-1]:
        if not isinstance(key, int) and bool(match(r'\[.*\]', key)):
            key_int = int(key.strip('[]'))
            while len(dic) <= key_int:
                dic.append({})
            dic = dic[key_int]
        else:
            if key not in dic:
                next_key = keys[keys.index(key)+1]
                if not isinstance(next_key, int) and bool(match(r'\[.*\]', next_key)):
                    dic[key] = []
                else:
                    dic[key] = {}
            dic = dic[key]
    last_key = keys[-1]
    if not isinstance(last_key, int) and bool(match(r'\[.*\]', last_key)):
        last_key_int = int(last_key.strip('[]'))
        while len(dic) <= last_key_int:
            dic.append(None)
        dic[last_key_int] = value
    else:
        dic[last_key] = value
