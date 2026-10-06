"""Тесты эмулятора командной строки (этапы 1-2)."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

import shell


def capture(func, *args):
	"""Вызвать функцию и вернуть результат и напечатанный текст."""
	buffer = io.StringIO()
	with redirect_stdout(buffer):
		result = func(*args)
	return result, buffer.getvalue().strip()


def run(line):
	"""Выполнить строку в эмуляторе и вернуть напечатанный текст."""
	return capture(shell.execute, line)[1]


def make_script(text):
	"""Создать временный файл стартового скрипта и вернуть путь."""
	file = tempfile.NamedTemporaryFile(
		"w", suffix=".txt", delete=False, encoding="utf-8")
	file.write(text)
	file.close()
	return file.name


class ParserTest(unittest.TestCase):
	"""Проверки парсера."""

	def test_split_by_spaces(self):
		"""Ввод делится на команду и аргументы по пробелам."""
		result = shell.parse_input("ls -l dir")
		self.assertEqual(result, ("ls", ["-l", "dir"]))

	def test_empty_line(self):
		"""Пустая строка не содержит команды."""
		self.assertEqual(shell.parse_input("   "), (None, []))

	def test_comment(self):
		"""Комментарий после # отбрасывается."""
		result = shell.parse_input("ls dir # комментарий")
		self.assertEqual(result, ("ls", ["dir"]))

	def test_prompt(self):
		"""Приглашение имеет вид username@hostname:~$."""
		prompt = shell.get_prompt()
		self.assertIn("@", prompt)
		self.assertTrue(prompt.endswith(":~$ "))


class CommandTest(unittest.TestCase):
	"""Проверки команд и обработки ошибок."""

	def test_ls(self):
		"""Заглушка ls выводит свои аргументы."""
		self.assertEqual(run("ls a b"), "ls: аргументы = ['a', 'b']")

	def test_cd(self):
		"""Заглушка cd выводит свой аргумент."""
		self.assertEqual(run("cd dir"), "cd: аргументы = ['dir']")

	def test_cd_too_many_args(self):
		"""cd с двумя аргументами сообщает об ошибке."""
		self.assertEqual(run("cd a b"), "cd: слишком много аргументов")

	def test_unknown_command(self):
		"""Неизвестная команда сообщает об ошибке."""
		self.assertEqual(run("hello"), "hello: команда не найдена")

	def test_exit(self):
		"""exit завершает работу с указанным кодом."""
		with self.assertRaises(SystemExit) as context:
			run("exit 3")
		self.assertEqual(context.exception.code, 3)

	def test_exit_bad_arg(self):
		"""exit с нечисловым аргументом сообщает об ошибке."""
		expected = "exit: abc: требуется числовой аргумент"
		self.assertEqual(run("exit abc"), expected)


class ConfigTest(unittest.TestCase):
	"""Проверки параметров и команды conf-dump."""

	def test_parse_args(self):
		"""Параметры --vfs и --script разбираются."""
		args = shell.parse_args(["--vfs", "a.xml", "--script", "s.txt"])
		self.assertEqual((args.vfs, args.script), ("a.xml", "s.txt"))

	def test_conf_dump(self):
		"""conf-dump выводит параметры в формате ключ=значение."""
		shell.CONFIG.update({"vfs": "a.xml", "script": None})
		self.assertEqual(run("conf-dump"), "vfs=a.xml\nscript=не задан")

	def test_conf_dump_args(self):
		"""conf-dump с аргументами сообщает об ошибке."""
		expected = "conf-dump: команда не принимает аргументы"
		self.assertEqual(run("conf-dump x"), expected)


class ScriptTest(unittest.TestCase):
	"""Проверки стартового скрипта."""

	def test_script_ok(self):
		"""Скрипт показывает ввод и вывод, комментарии пропускает."""
		path = make_script("# комментарий\nls a\n")
		result, output = capture(shell.run_script, path)
		os.remove(path)
		self.assertTrue(result)
		self.assertIn(shell.get_prompt() + "ls a", output)
		self.assertNotIn("комментарий", output)

	def test_script_error(self):
		"""Ошибка в скрипте сообщается с номером строки."""
		path = make_script("ls\nfoo\n")
		result, output = capture(shell.run_script, path)
		os.remove(path)
		self.assertFalse(result)
		self.assertIn("строка 2", output)

	def test_script_not_found(self):
		"""Отсутствующий скрипт вызывает сообщение об ошибке."""
		result, output = capture(shell.run_script, "no_such_file.txt")
		self.assertFalse(result)
		self.assertIn("не найден", output)


if __name__ == "__main__":
	unittest.main()