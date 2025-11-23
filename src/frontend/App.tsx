import { Hero } from './components/Hero';
import { Header } from './components/Header';
import { Features } from './components/Features';
import { Footer } from './components/Footer';
import { SearchServicePage } from './components/SearchServicePage';
import { ClinicDetailPage } from './components/ClinicDetailPage';
import { useState } from 'react';

export default function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'search-service' | 'check-medicine' | 'clinic-detail'>('home');
  const [selectedClinicId, setSelectedClinicId] = useState<string | null>(null);

  const handleNavigateToClinic = (clinicId: string) => {
    setSelectedClinicId(clinicId);
    setCurrentPage('clinic-detail');
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'search-service':
        return <SearchServicePage onBack={() => setCurrentPage('home')} onSelectClinic={handleNavigateToClinic} />;
      case 'clinic-detail':
        return <ClinicDetailPage clinicId={selectedClinicId!} onBack={() => setCurrentPage('search-service')} />;
      case 'check-medicine':
        return <div>Check Medicine Page (Coming Soon)</div>;
      default:
        return (
          <>
            <Hero onNavigate={setCurrentPage} />
            <Features />
            <Footer />
          </>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-950 via-green-900 to-green-950 relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-green-400 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-green-500 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-green-400 rounded-full blur-3xl"></div>
      </div>
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: `linear-gradient(rgb(134, 239, 172) 1px, transparent 1px), linear-gradient(90deg, rgb(134, 239, 172) 1px, transparent 1px)`,
        backgroundSize: '50px 50px'
      }}></div>
      
      <div className="relative z-10">
        <Header onNavigate={setCurrentPage} />
        {renderPage()}
      </div>
    </div>
  );
}

// No se hacer nada más