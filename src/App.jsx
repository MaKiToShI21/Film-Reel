import { useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import Footer from './components/Footer';
import Header from './components/Header';
import { FilmsProvider } from './context/FilmsContext';
import AboutPage from './pages/AboutPage';
import AddFilmPage from './pages/AddFilmPage';
import CatalogPage from './pages/CatalogPage';

export default function App() {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <FilmsProvider>
      <Header
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        onSearchSubmit={() => {}}
      />
      <main>
        <Routes>
          <Route
            path="/"
            element={
              <CatalogPage
                searchQuery={searchQuery}
                onSearchQueryChange={setSearchQuery}
                onSearchSubmit={() => {}}
              />
            }
          />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/add" element={<AddFilmPage />} />
        </Routes>
      </main>
      <Footer />
    </FilmsProvider>
  );
}
