const CURRENT_YEAR = new Date().getFullYear();

export function validateFilmForm(values) {
  const errors = {};

  const title = values.title.trim();
  if (!title) {
    errors.title = 'Название обязательно для заполнения.';
  } else if (title.length > 255) {
    errors.title = 'Длина названия превышает 255 символов.';
  }

  const year = Number(values.year);
  if (!values.year.toString().trim()) {
    errors.year = 'Год выпуска обязателен.';
  } else if (Number.isNaN(year) || !Number.isInteger(year)) {
    errors.year = 'Укажите корректный год.';
  } else if (year < 1888 || year > CURRENT_YEAR) {
    errors.year = `Год выпуска должен быть от 1888 до ${CURRENT_YEAR}.`;
  }

  const description = values.description.trim();
  if (!description) {
    errors.description = 'Описание обязательно для заполнения.';
  }

  if (!values.genreIds.length) {
    errors.genreIds = 'Укажите хотя бы один жанр.';
  }

  if (!values.tagIds.length) {
    errors.tagIds = 'Укажите хотя бы один тег.';
  }

  const duration = Number(values.duration);
  if (!values.duration.toString().trim()) {
    errors.duration = 'Длительность обязательна.';
  } else if (Number.isNaN(duration) || !Number.isInteger(duration) || duration < 1) {
    errors.duration = 'Длительность должна быть не менее 1 минуты.';
  }

  if (values.budget !== '' && Number(values.budget) < 0) {
    errors.budget = 'Бюджет не может быть отрицательным.';
  }

  if (values.boxOffice !== '' && Number(values.boxOffice) < 0) {
    errors.boxOffice = 'Сборы не могут быть отрицательными.';
  }

  return errors;
}
