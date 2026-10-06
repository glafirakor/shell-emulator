#!/bin/sh
# Проверка параметра --vfs
cd "$(dirname "$0")/../.." || exit 1
echo "=== 1. Запуск без параметров ==="
./run.sh < /dev/null
echo "=== 2. Указан путь к VFS ==="
./run.sh --vfs vfs/minimal.xml < /dev/null
echo "=== 3. Путь к VFS с пробелами ==="
./run.sh --vfs "my vfs/data.xml" < /dev/null