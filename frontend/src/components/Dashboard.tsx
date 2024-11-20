import React from 'react';
import {
    Music,
    Users,
    Search,
    User,
    Clock,
    Heart,
    Share2,
    Bell,
    Settings,
    SkipBack,
    SkipForward,
    Pause,
    Play
} from 'lucide-react';

const Dashboard = () => {
    // Données de démonstration
    const userProfile = {
        name: "John Doe",
        avatar: "/api/placeholder/40/40",
        currentlyPlaying: "No Time To Die - Billie Eilish"
    };

    const friendsList = [
        {
            id: 1,
            name: "Alice",
            avatar: "/api/placeholder/32/32",
            currentlyPlaying: "Run - Foo Fighters"
        },
        {
            id: 2,
            name: "Bob",
            avatar: "/api/placeholder/32/32",
            currentlyPlaying: "Blinding Lights - The Weeknd"
        },
        {
            id: 3,
            name: "Carol",
            avatar: "/api/placeholder/32/32",
            currentlyPlaying: "Bad Guy - Billie Eilish"
        },
    ];

    const recentTracks = [
        {id: 1, title: "Paradise", artist: "Coldplay", duration: "4:23"},
        {id: 2, title: "Take on Me", artist: "a-ha", duration: "3:46"},
        {id: 3, title: "Bohemian Rhapsody", artist: "Queen", duration: "5:55"},
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
            {/* Header avec profil utilisateur */}
            <header className="fixed top-0 left-0 right-0 z-50">
                <div>
                    <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-end ">
                        {/* Profil et actions à droite */}
                        <div className="flex items-center space-x-6">
                            <button className="hover:text-[#1DB954] transition-colors">
                                <Bell className="w-5 h-5"/>
                            </button>
                            <button className="hover:text-[#1DB954] transition-colors">
                                <Settings className="w-5 h-5"/>
                            </button>
                            <div
                                className="flex items-center gap-3 pl-6 border-l border-white/[0.06]">
                                <img
                                    src={userProfile.avatar}
                                    alt="Profile"
                                    className="w-8 h-8 rounded-full ring-2 ring-[#1DB954]"
                                />
                                <div className="hidden sm:block">
                                    <p className="text-sm font-medium">{userProfile.name}</p>
                                    <p className="text-xs text-gray-400 truncate max-w-[150px]">
                                        {userProfile.currentlyPlaying}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto pt-24 p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Column - Music Player & Recent */}
                <div className="space-y-6 md:col-span-2">
                    {/* Now Playing */}
                    <div className="p-6 rounded-xl bg-white/5 backdrop-blur-lg">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Music className="w-5 h-5 text-[#1DB954]"/>
                            Now Playing
                        </h3>
                        <div className="space-y-4">
                            <img
                                src="/api/placeholder/400/200"
                                alt="Album Cover"
                                className="w-full rounded-lg"
                            />
                            <div>
                                <h4 className="font-bold">No Time To Die</h4>
                                <p className="text-gray-400">Billie Eilish</p>
                            </div>
                            {/* Player Controls */}
                            <div className="space-y-2">
                                <div className="h-1 bg-gray-700 rounded-full">
                                    <div className="h-full w-1/3 bg-[#1DB954] rounded-full"></div>
                                </div>
                                <div className="flex justify-between text-sm text-gray-400">
                                    <span>1:23</span>
                                    <span>3:45</span>
                                </div>
                                <div className="flex justify-center items-center gap-4 py-2">
                                    <button className="p-2 hover:text-[#1DB954] transition-colors">
                                        <SkipBack className="w-5 h-5"/>
                                    </button>
                                    <button
                                        className="p-3 bg-[#1DB954] rounded-full hover:bg-[#1ed760] transition-colors">
                                        <Pause className="w-6 h-6"/>
                                    </button>
                                    <button className="p-2 hover:text-[#1DB954] transition-colors">
                                        <SkipForward className="w-5 h-5"/>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Recent Tracks */}
                    <div className="p-6 rounded-xl bg-white/5 backdrop-blur-lg">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Clock className="w-5 h-5 text-[#1DB954]"/>
                            Recent Tracks
                        </h3>
                        <div className="space-y-3">
                            {recentTracks.map(track => (
                                <div
                                    key={track.id}
                                    className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 transition-colors group"
                                >
                                    <div className="flex items-center gap-3">
                                        <button
                                            className="opacity-0 group-hover:opacity-100 transition-opacity">
                                            <Play className="w-4 h-4"/>
                                        </button>
                                        <div>
                                            <p className="font-medium">{track.title}</p>
                                            <p className="text-sm text-gray-400">{track.artist}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <span
                                            className="text-sm text-gray-400">{track.duration}</span>
                                        <button
                                            className="opacity-0 group-hover:opacity-100 transition-opacity hover:text-[#1DB954]">
                                            <Heart className="w-4 h-4"/>
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Column - Friends & Search */}
                <div className="space-y-6">
                    {/* Search Friends */}
                    <div className="p-6 rounded-xl bg-white/5 backdrop-blur-lg">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Search className="w-5 h-5 text-[#1DB954]"/>
                            Find Friends
                        </h3>
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Search by name or email..."
                                className="w-full bg-white/10 rounded-lg px-4 py-2 pl-10 focus:outline-none focus:ring-2 focus:ring-[#1DB954]"
                            />
                            <Search
                                className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"/>
                        </div>
                    </div>

                    {/* Friends List */}
                    <div className="p-6 rounded-xl bg-white/5 backdrop-blur-lg">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <Users className="w-5 h-5 text-[#1DB954]"/>
                            Friends
                        </h3>
                        <div className="space-y-4">
                            {friendsList.map(friend => (
                                <div
                                    key={friend.id}
                                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors group"
                                >
                                    <img
                                        src={friend.avatar}
                                        alt={friend.name}
                                        className="w-8 h-8 rounded-full"
                                    />
                                    <div className="flex-1 min-w-0">
                                        <p className="font-medium">{friend.name}</p>
                                        <p className="text-sm text-gray-400 truncate">{friend.currentlyPlaying}</p>
                                    </div>
                                    <button
                                        className="opacity-0 group-hover:opacity-100 transition-opacity hover:text-[#1DB954]">
                                        <Share2 className="w-4 h-4"/>
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;