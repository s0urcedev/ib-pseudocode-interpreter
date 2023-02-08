from code_entities import Code

if __name__ == "__main__":
    code = ""
    while True:
        try:
            line = input()
            if chr(3) not in line:
                code += line + "\n"
            else:
                break
        except:
            break
    Code(code).run()
