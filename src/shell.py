"""Эмулятор командной строки UNIX-подобной ОС (этап 1: REPL)."""

import getpass
import shlex
import socket

MAX_CD_ARGS = 1
MAX_EXIT_ARGS = 1


def get_prompt():
	"""Вернуть приглашение вида username@hostname:~$ из данных ОС."""
	username = getpass.getuser()
	hostname = socket.gethostname().split(".")[0]
	return f"{username}@{hostname}:~$ "


def parse_input(line):
	"""Разделить строку на команду и список аргументов."""
	try:
		tokens = shlex.split(line)
	except ValueError as error:
		print(f"ошибка разбора: {error}")
		return None, []
	if not tokens:
		return None, []
	return tokens[0], tokens[1:]


def cmd_ls(args):
	"""Заглушка ls: вывести имя команды и аргументы."""
	print(f"ls: аргументы = {args}")


def cmd_cd(args):
	"""Заглушка cd: вывести имя команды и аргумент."""
	if len(args) > MAX_CD_ARGS:
		print("cd: слишком много аргументов")
		return
	print(f"cd: аргументы = {args}")


def cmd_exit(args):
	"""Завершить работу эмулятора с необязательным кодом возврата."""
	if len(args) > MAX_EXIT_ARGS:
		print("exit: слишком много аргументов")
		return
	code = 0
	if args:
		if not args[0].lstrip("-").isdigit():
			print(f"exit: {args[0]}: требуется числовой аргумент")
			return
		code = int(args[0])
	print("выход из эмулятора")
	raise SystemExit(code)


COMMANDS = {
	"ls": cmd_ls,
	"cd": cmd_cd,
	"exit": cmd_exit,
}


def execute(line):
	"""Разобрать и выполнить одну строку ввода."""
	command, args = parse_input(line)
	if command is None:
		return
	handler = COMMANDS.get(command)
	if handler is None:
		print(f"{command}: команда не найдена")
		return
	handler(args)


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


if __name__ == "__main__":
	repl()