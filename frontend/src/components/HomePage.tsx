import React from 'react';

const HomePage = () => {
    const letters = ['S', 'y', 'n', 'c', 'i', 'f', 'y'];
    const LETTER_STAGGER = 150;
    const SEQUENCE_START_DELAY = 2000;

    const buttonClass = `
        w-12 h-12 flex items-center justify-center
        text-white font-bold rounded-full
        transition-all duration-300
        hover:scale-105 hover:shadow-lg
        animate-[fadeIn_1s_ease-out_forwards]
    `;

    return (
        <div className="min-h-[80vh] flex flex-col items-center justify-center">
            <div className="text-center space-y-12 w-full max-w-xl mx-auto px-4">
                <h1
                    className="text-7xl font-bold tracking-tight relative"
                    style={{
                        perspective: '1000px',
                        transformStyle: 'preserve-3d'
                    }}
                >
                    {letters.map((letter, index) => {
                        const jumpInDelay = index * LETTER_STAGGER;
                        const sequenceDelay = SEQUENCE_START_DELAY + (index * LETTER_STAGGER);

                        return (
                            <span
                                key={index}
                                className={`
                                    relative inline-block opacity-0
                                    [backface-visibility:hidden] [will-change:transform]
                                    [transform-origin:center_bottom]
                                    animate-[jumpIn_0.8s_cubic-bezier(0.2,0.8,0.2,1)_forwards]
                                `}
                                style={{
                                    animationDelay: `${jumpInDelay}ms`,
                                }}
                            >
                                <span
                                    className={`
                                        relative inline-block transition-all duration-100
                                        hover:text-[#1DB954] hover:translate-y-[-12px]
                                        hover:scale-[1.3] hover:[filter:drop-shadow(0_0_16px_rgba(29,185,84,0.6))]
                                    `}
                                    style={{
                                        animation: `highlight 1s ease-out forwards ${sequenceDelay}ms`,
                                    }}
                                >
                                    {letter}
                                </span>
                            </span>
                        );
                    })}
                </h1>

                <p
                    className="text-muted-foreground text-lg animate-[fadeIn_1s_ease-out_forwards]"
                    style={{
                        animationDelay: '1.2s',
                        opacity: 0
                    }}
                >
                    Share music with your friends. Together.
                </p>

                <div className="flex flex-col items-center">
                    <p
                        className="text-xl font-bold mb-4 tracking-wider animate-[fadeIn_1s_ease-out_forwards]"
                        style={{
                            animationDelay: '1.6s',
                            opacity: 0
                        }}
                    >
                        Connect with
                    </p>
                    <div className="flex flex-row items-center space-x-4">
                        <button
                            className={`${buttonClass} bg-[#1DB954] hover:bg-[#1ed760]`}
                            style={{
                                animationDelay: '1.8s',
                                opacity: 0
                            }}
                        >
                            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                            </svg>
                        </button>
                        <button
                            className={`${buttonClass} bg-red-600 hover:bg-red-700`}
                            style={{
                                animationDelay: '2s',
                                opacity: 0
                            }}
                        >
                            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                            </svg>
                        </button>
                        <button
                            className={`${buttonClass} bg-[#a83cfc] hover:bg-[#B355E8]`}
                            style={{
                                animationDelay: '2.2s',
                                opacity: 0
                            }}
                        >
                            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M22.5 10.5h-1.5V12h1.5v-1.5zm-4.5-3V9h1.5V7.5H18zm0 3V12h1.5v-1.5H18zm-3-3V9h1.5V7.5H15zm0 3V12h1.5v-1.5H15zm-3-3V9h1.5V7.5H12zm0 3V12h1.5v-1.5H12zm-3-3V9h1.5V7.5H9zm0 3V12h1.5v-1.5H9zm-3-3V9h1.5V7.5H6zm0 3V12h1.5v-1.5H6zm-3-3V9h1.5V7.5H3zm0 3V12h1.5v-1.5H3z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;