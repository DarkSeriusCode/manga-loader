
def level_fabric(color: str, symbol: str):
    def new_level(text: str):
        print(f"{color}\033[1m{symbol} \033[0m{text}")
    return new_level


info = level_fabric("\033[36m", "[@]")
error = level_fabric("\033[31m", "[!]")
trace = level_fabric("\033[32m", "[+]")
