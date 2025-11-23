import { ReactNode } from 'react';

interface ActionButtonProps {
  icon: ReactNode;
  label: string;
  onClick: () => void;
  variant: 'primary' | 'secondary';
}

export function ActionButton({ icon, label, onClick, variant }: ActionButtonProps) {
  const baseStyles = "group relative px-12 py-6 rounded-2xl transition-all duration-300 flex items-center gap-4 min-w-[280px] justify-center overflow-hidden shadow-xl";
  
  const variantStyles = {
    primary: "bg-gradient-to-r from-green-500 via-green-400 to-green-500 text-white hover:shadow-2xl hover:scale-105 border-2 border-transparent hover:shadow-green-500/30",
    secondary: "bg-gradient-to-r from-black via-gray-900 to-black text-white hover:shadow-2xl hover:scale-105 border-2 border-green-400/50 hover:border-green-400"
  };

  return (
    <button
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]}`}
    >
      {/* Shine effect on hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-30 transform -skew-x-12 group-hover:translate-x-full transition-transform duration-700"></div>
      
      <span className="relative z-10">{icon}</span>
      <span className="relative z-10 text-lg">{label}</span>
    </button>
  );
}