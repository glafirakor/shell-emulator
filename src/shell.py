"""Эмулятор командной строки UNIX-подобной ОС (этапы 1-2)."""

import argparse
import getpass
import shlex
import socket

MAX_CD_ARGS = 1
MAX_EXIT_ARGS = 1
COMMENT_CHAR = "#"

CONFIG = {
	"vfs": None,
	"script": None,
}


def get_prompt():
	"""Вернуть приглашение вида username@hostname:~$ из данных ОС."""
	username = getpass.getuser()
	hostname = socket.gethostname().split(".")[0]
	return f"{username}@{hostname}:~$ "


def parse_input(line):
	"""Разделить строку на команду и аргументы, отбросив комментарий."""
	tokens = shlex.split(line, comments=True)
	if not tokens:
		return None, []
	return tokens[0], tokens[1:]


def config_lines():
	"""Вернуть параметры эмулятора в виде строк ключ=значение."""
	return [f"{key}={value or 'не задан'}" for key, value in CONFIG.items()]


def cmd_ls(args):
	"""Заглушка ls: вывести имя команды и аргументы."""
	print(f"ls: аргументы = {args}")
	return True


def cmd_cd(args):
	"""Заглушка cd: вывести имя команды и аргумент."""
	if len(args) > MAX_CD_ARGS:
		print("cd: слишком много аргументов")
		return False
	print(f"cd: аргументы = {args}")
	return True


def cmd_exit(args):
	"""Завершить работу эмулятора с необязательным кодом возврата."""
	if len(args) > MAX_EXIT_ARGS:
		print("exit: слишком много аргументов")
		return False
	code = 0
	if args:
		if not args[0].lstrip("-").isdigit():
			print(f"exit: {args[0]}: требуется числовой аргумент")
			return False
		code = int(args[0])
	print("выход из эмулятора")
	raise SystemExit(code)


def cmd_conf_dump(args):
	"""Служебная команда: вывести параметры эмулятора."""
	if args:
		print("conf-dump: команда не принимает аргументы")
		return False
	for line in config_lines():
		print(line)
	return True


COMMANDS = {
	"ls": cmd_ls,
	"cd": cmd_cd,
	"exit": cmd_exit,
	"conf-dump": cmd_conf_dump,
}


def execute(line):
	"""Выполнить строку ввода; вернуть True, если ошибок не было."""
	try:
		command, args = parse_input(line)
	except ValueError as error:
		print(f"ошибка разбора: {error}")
		return False
	if command is None:
		return True
	handler = COMMANDS.get(command)
	if handler is None:
		print(f"{command}: команда не найдена")
		return False
	return handler(args)


def read_script(path):
	"""Прочитать строки стартового скрипта; вернуть None при ошибке."""
	try:
		with open(path, encoding="utf-8") as file:
			return file.read().splitlines()
	except FileNotFoundError:
		print(f"ошибка: стартовый скрипт не найден: {path}")
	except OSError as error:
		print(f"ошибка: не удалось прочитать стартовый скрипт: {error}")
	return None


def run_script(path):
	"""Выполнить стартовый скрипт, показывая ввод и вывод как диалог."""
	lines = read_script(path)
	if lines is None:
		return False
	success = True
	for number, line in enumerate(lines, start=1):
		text = line.strip()
		if not text or text.startswith(COMMENT_CHAR):
			continue
		print(f"{get_prompt()}{text}")
		if not execute(text):
			print(f"ошибка в стартовом скрипте {path}, строка {number}")
			success = False
	return success


def repl():
	"""Главный цикл: чтение строки, выполнение, вывод результата."""
	while True:
		try:
			line = input(get_prompt())
		except EOFError:
			print()
			break
		except KeyboardInterrupt:
			print()
			continue
		execute(line)


def parse_args(argv=None):
	"""Разобрать параметры командной строки эмулятора."""
	parser = argparse.ArgumentParser(description="Эмулятор командной строки")
	parser.add_argument("--vfs", help="путь к физическому расположению VFS")
	parser.add_argument("--script", help="путь к стартовому скрипту")
	return parser.parse_args(argv)


def main(argv=None):
	"""Точка входа: параметры, отладочный вывод, скрипт, затем REPL."""
	args = parse_args(argv)
	CONFIG["vfs"] = args.vfs
	CONFIG["script"] = args.script
	for line in config_lines():
		print(f"[debug] {line}")
	if args.script:
		run_script(args.script)
	repl()


if __name__ == "__main__":
	main()