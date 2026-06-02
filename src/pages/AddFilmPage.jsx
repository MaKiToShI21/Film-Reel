import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import FormField from '../components/FormField';
import PickerField from '../components/PickerField';
import { useFilms } from '../context/FilmsContext';
import { validateFilmForm } from '../utils/validation';

const emptyForm = {
  title: '',
  year: '',
  description: '',
  budget: '',
  boxOffice: '',
  duration: '',
  filmingLocation: '',
  genreIds: [],
  directorIds: [],
  tagIds: [],
  posterUrl: '',
};

function toggleId(list, id) {
  return list.includes(id) ? list.filter((item) => item !== id) : [...list, id];
}

export default function AddFilmPage() {
  const navigate = useNavigate();
  const { addFilm, genres, directors, tags } = useFilms();
  const [values, setValues] = useState(emptyForm);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [posterPreview, setPosterPreview] = useState('');

  const updateField = (field, value) => {
    setValues((current) => ({ ...current, [field]: value }));
  };

  const markTouched = (field) => {
    setTouched((current) => ({ ...current, [field]: true }));
  };

  const validateAndSetErrors = (nextValues = values) => {
    const nextErrors = validateFilmForm(nextValues);
    setErrors(nextErrors);
    return nextErrors;
  };

  const handleBlur = (field) => {
    markTouched(field);
    validateAndSetErrors();
  };

  const handlePosterChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) {
      setPosterPreview('');
      updateField('posterUrl', '');
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    setPosterPreview(objectUrl);
    updateField('posterUrl', objectUrl);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const nextErrors = validateAndSetErrors();
    setTouched({
      title: true,
      year: true,
      description: true,
      duration: true,
      genreIds: true,
      tagIds: true,
      budget: true,
      boxOffice: true,
    });

    if (Object.keys(nextErrors).length) {
      return;
    }

    addFilm(values);
    navigate('/');
  };

  const showError = (field) => (touched[field] ? errors[field] : '');

  return (
    <section className="film-form-page">
      <div className="film-form-card">
        <header className="film-form-header">
          <h1>Добавить фильм</h1>
          <p className="film-form-subtitle">
            Заполните форму — новая запись появится в каталоге без перезагрузки страницы.
          </p>
        </header>

        <form className="film-form" onSubmit={handleSubmit} noValidate>
          {Object.keys(errors).length > 0 &&
            Object.values(touched).some(Boolean) &&
            Object.keys(validateFilmForm(values)).length > 0 && (
              <ul className="film-form-errors film-form-errors--global">
                <li>Проверьте выделенные поля и исправьте ошибки.</li>
              </ul>
            )}

          <fieldset className="film-form-section">
            <legend className="film-form-section-title">Основная информация</legend>
            <div className="film-form-grid">
              <FormField
                id="film-title"
                label="Название"
                value={values.title}
                onChange={(event) => updateField('title', event.target.value)}
                onBlur={() => handleBlur('title')}
                error={showError('title')}
              />
              <FormField
                id="film-year"
                label="Год выпуска"
                value={values.year}
                onChange={(event) => updateField('year', event.target.value)}
                onBlur={() => handleBlur('year')}
                error={showError('year')}
                inputProps={{
                  inputMode: 'numeric',
                  maxLength: 4,
                  placeholder: String(new Date().getFullYear()),
                }}
              />
            </div>

            <div className={showError('posterUrl') ? 'film-form-field film-form-field--poster film-form-field--error' : 'film-form-field film-form-field--poster'}>
              <span className="film-form-label">Постер</span>
              <div className="film-form-poster-box">
                {posterPreview && (
                  <img src={posterPreview} alt="Предпросмотр постера" className="film-form-poster-preview" />
                )}
                <input
                  type="file"
                  accept="image/*"
                  className="film-form-file-input"
                  onChange={handlePosterChange}
                />
              </div>
            </div>

            <FormField
              id="film-description"
              label="Описание"
              value={values.description}
              onChange={(event) => updateField('description', event.target.value)}
              onBlur={() => handleBlur('description')}
              error={showError('description')}
            >
              <textarea
                id="film-description"
                className="film-form-input"
                rows={5}
                value={values.description}
                onChange={(event) => updateField('description', event.target.value)}
                onBlur={() => handleBlur('description')}
              />
            </FormField>
          </fieldset>

          <fieldset className="film-form-section">
            <legend className="film-form-section-title">Технические детали</legend>
            <div className="film-form-grid">
              <FormField
                id="film-budget"
                label="Бюджет ($)"
                type="number"
                value={values.budget}
                onChange={(event) => updateField('budget', event.target.value)}
                onBlur={() => handleBlur('budget')}
                error={showError('budget')}
                inputProps={{ min: '0', step: '0.01' }}
              />
              <FormField
                id="film-box-office"
                label="Сборы ($)"
                type="number"
                value={values.boxOffice}
                onChange={(event) => updateField('boxOffice', event.target.value)}
                onBlur={() => handleBlur('boxOffice')}
                error={showError('boxOffice')}
                inputProps={{ min: '0', step: '0.01' }}
              />
            </div>
            <div className="film-form-grid">
              <FormField
                id="film-duration"
                label="Длительность (мин)"
                type="number"
                value={values.duration}
                onChange={(event) => updateField('duration', event.target.value)}
                onBlur={() => handleBlur('duration')}
                error={showError('duration')}
                inputProps={{ min: '1', step: '1' }}
              />
              <FormField
                id="film-location"
                label="Место съёмок"
                value={values.filmingLocation}
                onChange={(event) => updateField('filmingLocation', event.target.value)}
                onBlur={() => handleBlur('filmingLocation')}
              />
            </div>
          </fieldset>

          <fieldset className="film-form-section">
            <legend className="film-form-section-title">Классификация</legend>
            <PickerField
              label="Жанры"
              items={genres}
              selectedIds={values.genreIds}
              onToggle={(id) => {
                const nextGenreIds = toggleId(values.genreIds, id);
                updateField('genreIds', nextGenreIds);
                markTouched('genreIds');
                validateAndSetErrors({ ...values, genreIds: nextGenreIds });
              }}
              error={showError('genreIds')}
            />
            <PickerField
              label="Режиссёры"
              items={directors}
              selectedIds={values.directorIds}
              onToggle={(id) => updateField('directorIds', toggleId(values.directorIds, id))}
            />
            <PickerField
              label="Теги"
              items={tags}
              selectedIds={values.tagIds}
              nameKey="tag"
              onToggle={(id) => {
                const nextTagIds = toggleId(values.tagIds, id);
                updateField('tagIds', nextTagIds);
                markTouched('tagIds');
                validateAndSetErrors({ ...values, tagIds: nextTagIds });
              }}
              error={showError('tagIds')}
            />
          </fieldset>

          <div className="film-form-actions">
            <button type="submit" className="btn film-form-submit">
              Сохранить
            </button>
            <Link to="/" className="film-form-cancel">
              Отмена
            </Link>
          </div>
        </form>
      </div>
    </section>
  );
}
