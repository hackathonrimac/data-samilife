import { Search, Shield, Clock } from 'lucide-react';
import { FeatureCard } from './FeatureCard';

export function Features() {
  const features = [
    {
      icon: <Search className="w-8 h-8" />,
      title: "Smart Search",
      description: "Advanced AI-powered search to find the perfect clinic or medication for your needs"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Verified Information",
      description: "All clinics and medications are verified and updated regularly for accuracy"
    },
    {
      icon: <Clock className="w-8 h-8" />,
      title: "24/7 Available",
      description: "Access our platform anytime, anywhere to get the healthcare information you need"
    }
  ];

  return (
    <section className="py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl text-center mb-4 text-green-100">Why Choose SamiLife?</h2>
        <p className="text-center text-green-300 mb-12 max-w-2xl mx-auto">
          We provide the most comprehensive and reliable healthcare search platform
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
}