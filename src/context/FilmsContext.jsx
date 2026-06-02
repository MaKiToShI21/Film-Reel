import { createContext, useContext, useMemo, useState } from 'react';
import { directors, genres, initialFilms, tags } from '../data/catalogData';

const FilmsContext = createContext(null);

let nextFilmId = initialFilms.length + 1;

export function FilmsProvider({ children }) {
  const [films, setFilms] = useState(initialFilms);

  const addFilm = (filmData) => {
    const newFilm = {
      id: nextFilmId++,
      title: filmData.title.trim(),
      year: Number(filmData.year),
      rating: 0,
      description: filmData.description.trim(),
      poster: filmData.posterUrl || '',
      addedAt: new Date().toISOString(),
      genreIds: filmData.genreIds,
      directorIds: filmData.directorIds,
      tagIds: filmData.tagIds,
      details: {
        budget: filmData.budget === '' ? null : Number(filmData.budget),
        boxOffice: filmData.boxOffice === '' ? null : Number(filmData.boxOffice),
        duration: Number(filmData.duration),
        filmingLocation: filmData.filmingLocation.trim(),
      },
    };

    setFilms((current) => [newFilm, ...current]);
    return newFilm;
  };

  const value = useMemo(
    () => ({
      films,
      genres,
      directors,
      tags,
      addFilm,
    }),
    [films],
  );

  return <FilmsContext.Provider value={value}>{children}</FilmsContext.Provider>;
}

export function useFilms() {
  const context = useContext(FilmsContext);
  if (!context) {
    throw new Error('useFilms must be used within FilmsProvider');
  }
  return context;
}
