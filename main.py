import os
import sys


def search():
    # 字符串处理
    argv_list = [argv.replace('\\', '\\\\') for argv in sys.argv]
    args1 = argv_list[1]

    if "'" in args1:
        print(f'查询语句：find . -type f | xargs grep "{args1}"')
        # 查找
        output = os.popen(f'find . -type f | xargs grep "{args1}"').read()
        print("查找结果：\n", output)
    else:
        print(f"查询语句：find . -type f | xargs grep '{args1}'")
        # 查找
        output = os.popen(f"find . -type f | xargs grep '{args1}'").read()
        print("查找结果：\n", output)


def file_create():
    # 创建一个带有args1的新文件，测试命令是否能成功
    if not os.path.exists("testdir"):
        os.makedirs("testdir")
    os.system("touch testdir/before.txt")
    with open('testdir/before.txt', 'w') as f:
        f.write(sys.argv[1])
    with open('testdir/before.txt', 'r') as f:
        before = f.read()
    print("原始串:", before)


def get_command():
    # 字符串处理
    argv_list = [argv.replace('\\', r'\\\\\\') for argv in sys.argv]
    argv_list = [argv.replace('"', r'\"') for argv in argv_list]
    argv_list = [argv.replace("{", r"\{") for argv in argv_list]
    argv_list = [argv.replace("}", r"\}") for argv in argv_list]

    args1 = argv_list[1]
    args2 = argv_list[2]

    # 替换
    comm_str = sys.argv[1] + sys.argv[2]

    if '/' not in comm_str:
        if "'" in comm_str and '\\' not in comm_str:

            if "'" in comm_str and '"' in comm_str:
                # 单引号双引号都有，需要转义
                argv_list = [argv.replace('"', r'\\"') for argv in argv_list]
                args1 = argv_list[1]
                args2 = argv_list[2]
            # 有单引号，必须用双引号
            print(f"""替换语句1：echo "replacestr \\"s/{args1}/{args2}/g\\"" | pbcopy""")
            # 字符串赋值
            file_test_command = f'find testdir -type f -print0 | xargs -0 gsed -i \\"s/{args1}/{args2}/g\\"'
            real_replace_command = f'find . -type f -print0 | xargs -0 gsed -i \\"s/{args1}/{args2}/g\\"'
            copyboard = f"""echo "replacestr \\"s/{args1}/{args2}/g\\"" | pbcopy"""
        else:
            # 有反斜杠，必须用单引号
            print(f"""替换语句2：echo "replacestr 's/{args1}/{args2}/g'" | pbcopy""")
            # 字符串赋值
            file_test_command = f"find testdir -type f -print0 | xargs -0 gsed -i 's/{args1}/{args2}/g'"
            real_replace_command = f"find . -type f -print0 | xargs -0 gsed -i 's/{args1}/{args2}/g'"
            copyboard = rf"""echo "replacestr 's/{args1}/{args2}/g'" | pbcopy"""
    else:
        if "'" in comm_str and '\\' not in comm_str:
            if "'" in comm_str and '"' in comm_str:
                # 单引号双引号都有，需要转义
                argv_list = [argv.replace('"', r'\\"') for argv in argv_list]
                args1 = argv_list[1]
                args2 = argv_list[2]
            # 有单引号，必须用双引号
            print(f"""替换语句3：echo "replacestr \\"s|{args1}|{args2}|g\\"" | pbcopy""")
            # 字符串赋值
            file_test_command = f'find testdir -type f -print0 | xargs -0 gsed -i \\"s|{args1}|{args2}|g\\"'
            real_replace_command = f'find . -type f -print0 | xargs -0 gsed -i \\"s|{args1}|{args2}|g\\"'
            copyboard = f"""echo "replacestr \\"s|{args1}|{args2}|g\\"" | pbcopy"""
        else:
            # 有反斜杠，必须用单引号
            print(f"""替换语句4：echo "replacestr 's|{args1}|{args2}|g'" | pbcopy""")
            # 字符串赋值
            file_test_command = f"find testdir -type f -print0 | xargs -0 gsed -i 's|{args1}|{args2}|g'"
            real_replace_command = f"find . -type f -print0 | xargs -0 gsed -i 's|{args1}|{args2}|g'"
            copyboard = f"""echo "replacestr 's|{args1}|{args2}|g'" | pbcopy"""
    return file_test_command, real_replace_command, copyboard


def replace():
    choose = input("\n是否替换？(y/n): ")
    if choose == 'y':
        os.system(real_replace_command)


def file_test_result():
    os.system(file_test_command)
    # 比对结果
    with open('testdir/before.txt', 'r') as f:
        after = f.read()
    print("换后串:", after)

def file_delete():
    if os.path.exists("testdir"):
        os.system("rm -rf testdir")


if __name__ == '__main__':
    print("\n=========================================查询===========================================")
    search()
    print("=========================================替换===========================================")
    if len(sys.argv) > 2:
        command = get_command()
        file_test_command = command[0]
        real_replace_command = command[1]
        copyboard = command[2]

        file_create()
        file_test_result()
        file_delete()
        replace()

    print("\n=========================================检验===========================================")
    search()