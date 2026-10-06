#!/bin/sh
# Проверка параметра --script
cd "$(dirname "$0")/../.." || exit 1
echo "=== 1. Стартовый скрипт без ошибок ==="
./run.sh --script tests/scripts/startup.txt < /dev/null
echo "=== 2. Стартовый скрипт с ошибками ==="
./run.sh --script tests/scripts/errors.txt < /dev/null
echo "=== 3. Несуществующий стартовый скрипт ==="
./run.sh --script tests/scripts/no_such_file.txt < /dev/null