from django.core.exceptions import ValidationError
import re


def validate_full_name(full_name: str) -> ValidationError | None:
  """Валидирует ФИО."""

  if not re.match(r'^[А-Яа-я\- ]+$', full_name):
    raise ValidationError("Используйте только РУССКИЙ алфавит для написания ФИО")

  parts = full_name.split()
  if len(parts) < 3:
    raise ValidationError("Фамилия, Имя и Отчество должны быть введены через пробел")

  for part in parts:
    if len(part) < 2:
      raise ValidationError("Введите настоящее ФИО")
