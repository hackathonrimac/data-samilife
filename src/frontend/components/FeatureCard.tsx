import { ReactNode } from 'react';

interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
}

export function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="group bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-8 border border-green-700/30 hover:border-green-500/50 transition-all duration-300 hover:transform hover:scale-105">
      <div className="bg-gradient-to-br from-green-400 to-green-600 text-white w-16 h-16 rounded-xl flex items-center justify-center mb-4 group-hover:shadow-lg group-hover:shadow-green-500/30 transition-shadow">
        {icon}
      </div>
      <h3 className="text-xl text-white mb-2">{title}</h3>
      <p className="text-green-200 leading-relaxed">{description}</p>
    </div>
  );
}