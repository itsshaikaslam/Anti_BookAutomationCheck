import React, { useState } from 'react';

const App: React.FC = () => {
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);

    const handleGenerate = async () => {
        if (!topic) return;
        setLoading(true);
        try {
            const res = await fetch('/api/generations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic_sentence: topic }),
            });
            const data = await res.json();
            alert(`Generation started! ID: ${data.id}`);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen p-8 bg-neo-white">
            <header className="mb-12 border-b-8 border-neo-black pb-4">
                <h1 className="text-6xl tracking-tighter">ANTIGRAVITY BOOKMAKER</h1>
                <p className="text-xl font-mono mt-2 bg-neo-cyan inline-block px-2">AUTOMATED_EBOOK_SYSTEM_V1.0</p>
            </header>

            <main className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <section className="neo-card flex flex-col gap-6">
                    <h2 className="text-3xl bg-neo-pink text-white inline-block w-fit px-2">New Generation</h2>
                    <div className="flex flex-col gap-2">
                        <label className="font-bold">TOPIC SENTENCE</label>
                        <textarea
                            className="neo-input h-32"
                            placeholder="Enter your ebook topic or detailed description..."
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                        />
                    </div>
                    <button
                        className="neo-button text-2xl"
                        onClick={handleGenerate}
                        disabled={loading}
                    >
                        {loading ? 'INITIALIZING AGENTS...' : 'LAUNCH PIPELINE'}
                    </button>
                </section>

                <section className="flex flex-col gap-8">
                    <div className="neo-card bg-neo-black text-neo-white font-mono h-64 overflow-hidden">
                        <div className="flex justify-between items-center border-b border-gray-700 pb-2 mb-4">
                            <span className="text-xs uppercase">Agent Swarm Terminal</span>
                            <div className="flex gap-2">
                                <div className="w-3 h-3 bg-red-500 rounded-full" />
                                <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                                <div className="w-3 h-3 bg-green-500 rounded-full" />
                            </div>
                        </div>
                        <div className="text-sm opacity-80">
                            <p>[09:12:04] > INITIALIZING CORE_ORCHESTRATOR</p>
                            <p>[09:12:05] > LOADING_MODELS: LLAMA3.1, SD-XL</p>
                            <p>[09:12:07] > WAITING_FOR_TOPIC_INPUT...</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="neo-card bg-neo-yellow">
                            <h3 className="text-lg">Storage</h3>
                            <p className="text-sm font-mono mt-1">DUAL_SYNC:_ACTIVE</p>
                        </div>
                        <div className="neo-card bg-neo-cyan">
                            <h3 className="text-lg">Network</h3>
                            <p className="text-sm font-mono mt-1">LATENCY:_24MS</p>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
};

export default App;
