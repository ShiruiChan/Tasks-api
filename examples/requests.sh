#!/usr/bin/env bash
# Примеры запросов к Tasks API через curl.
# Замените BASE на адрес вашего деплоя, например:
#   BASE="https://tasks-api.onrender.com"
BASE="${BASE:-http://localhost:8000}"

echo "== Проверка здоровья сервиса =="
curl -s "$BASE/health"
echo

echo "== Создание задачи =="
curl -s -X POST "$BASE/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Сделать проект", "description": "Тестирование и деплой"}'
echo

echo "== Список задач =="
curl -s "$BASE/tasks"
echo

echo "== Получить задачу по id =="
curl -s "$BASE/tasks/1"
echo

echo "== Отметить задачу выполненной =="
curl -s -X PATCH "$BASE/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
echo

echo "== Удалить задачу =="
curl -s -o /dev/null -w "HTTP %{http_code}\n" -X DELETE "$BASE/tasks/1"
