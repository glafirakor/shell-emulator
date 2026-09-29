"""Тесты эмулятора командной строки (этап 1)."""

import io
import unittest
from contextlib import redirect_stdout

import shell


def run(line):
	"""Выполнить строку в эмуляторе и вернуть напечатанный текст."""
	buffer = io.StringIO()
	with redirect_stdout(buffer):
		shell.execute(line)
	return buffer.getvalue().strip()


class ParserTest(unittest.TestCase):
	"""Проверки парсера."""

	def test_split_by_spaces(self):
		"""Ввод делится на команду и аргументы по пробелам."""
		result = shell.parse_input("ls -l dir")
		self.assertEqual(result, ("ls", ["-l", "dir"]))

	def test_empty_line(self):
		"""Пустая строка не содержит команды."""
		self.assertEqual(shell.parse_input("   "), (None, []))

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


if __name__ == "__main__":
	unittest.main()