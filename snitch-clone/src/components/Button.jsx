export default function Button({ children, variant = 'primary', className = '', ...props }) {
  const baseClasses = 'px-6 py-3 text-xs font-bold uppercase tracking-wider transition-colors focus:outline-none flex justify-center items-center';
  
  const variants = {
    primary: 'bg-black text-white hover:bg-opacity-90',
    secondary: 'bg-transparent border border-black text-black hover:bg-snitch-surface',
    outline: 'bg-white border border-snitch-border text-black hover:border-black',
  };

  return (
    <button 
      className={`${baseClasses} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
