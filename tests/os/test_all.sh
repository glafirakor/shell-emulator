#!/bin/sh
# Проверка всех параметров вместе и ошибок в параметрах
cd "$(dirname "$0")/../.." || exit 1
echo "=== 1. Оба параметра ==="
./run.sh --vfs vfs/minimal.xml --script tests/scripts/startup.txt < /dev/null
echo "=== 2. Справка по параметрам ==="
./run.sh --help
echo "=== 3. Неизвестный параметр ==="
./run.sh --foo bar