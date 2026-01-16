import React, { useState, useEffect } from 'react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

interface Generation {
    id: number;
    status: string;
    progress: number;
    current_agent?: string;
}

const App: React.FC = () => {
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);
    const [activeGenId, setActiveGenId] = useState<number | null>(null);
    const [activeGen, setActiveGen] = useState<Generation | null>(null);
    const [logs, setLogs] = useState<string[]>([
        '[SYSTEM] > INITIALIZING CORE_ORCHESTRATOR',
        '[SYSTEM] > LOADING_MODELS: LLAMA3.1, SD-XL',
        '[SYSTEM] > WAITING_FOR_TOPIC_INPUT...'
    ]);

    const addLog = (msg: string) => {
        setLogs(prev => [...prev.slice(-10), `[${new Date().toLocaleTimeString()}] > ${msg}`]);
    }

    const handleGenerate = async () => {
        if (!topic) return;
        setLoading(true);
        addLog(`REQUESTING_GENERATION: "${topic.substring(0, 30)}..."`);

        try {
            const res = await fetch(`${API_BASE}/generations/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic_sentence: topic }),
            });
            if (!res.ok) throw new Error('Failed to start generation');

            const data = await res.json();
            setActiveGenId(data.id);
            addLog(`GENERATION_STARTED: ID_${data.id}`);
        } catch (err) {
            console.error(err);
            addLog(`ERROR: ${err instanceof Error ? err.message : 'Unknown error'}`);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        let interval: any;
        if (activeGenId) {
            interval = setInterval(async () => {
                try {
                    const res = await fetch(`${API_BASE}/generations/${activeGenId}`);
                    if (res.ok) {
                        const data = await res.json();
                        setActiveGen(data);
                        if (data.current_agent) {
                            addLog(`AGENT_ACTIVE: ${data.current_agent} (${data.progress}%)`);
                        }
                        if (data.status === 'completed' || data.status === 'failed') {
                            clearInterval(interval);
                            setActiveGenId(null);
                            addLog(`PROCESS_FINISHED: STATUS_${data.status.toUpperCase()}`);
                        }
                    }
                } catch (err) {
                    console.error(err);
                }
            }, 3000);
        }
        return () => clearInterval(interval);
    }, [activeGenId]);

    return (
        <div className="min-h-screen p-8 bg-neo-white font-sans">
            <header className="mb-12 border-b-8 border-neo-black pb-4">
                <h1 className="text-6xl tracking-tighter font-black">ANTIGRAVITY BOOKMAKER</h1>
                <p className="text-xl font-mono mt-2 bg-neo-cyan inline-block px-2 border-2 border-neo-black">
                    V1.0_STABLE_AI_ENGINE
                </p>
            </header>

            <main className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <section className="neo-card flex flex-col gap-6">
                    <h2 className="text-3xl bg-neo-pink text-white inline-block w-fit px-2">New Generation</h2>
                    <div className="flex flex-col gap-2">
                        <label className="font-bold text-sm uppercase tracking-widest text-gray-600">Topic Sentence / Prompt</label>
                        <textarea
                            className="neo-input h-32 text-lg"
                            placeholder="Enter your ebook topic or detailed description..."
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            disabled={!!activeGenId}
                        />
                    </div>
                    <button
                        className={`neo-button text-2xl ${activeGenId ? 'bg-gray-300 pointer-events-none' : ''}`}
                        onClick={handleGenerate}
                        disabled={loading || !!activeGenId}
                    >
                        {loading ? 'COMMUNICATING...' : activeGenId ? 'PIPELINE_RUNNING' : 'LAUNCH PIPELINE'}
                    </button>

                    {activeGen && (
                        <div className="mt-4 border-t-4 border-neo-black pt-4">
                            <div className="flex justify-between items-end mb-2">
                                <span className="font-bold uppercase tracking-tighter">Overall Progress</span>
                                <span className="font-mono text-2xl">{activeGen.progress}%</span>
                            </div>
                            <div className="h-8 bg-neo-black border-2 border-neo-black p-1">
                                <div
                                    className="h-full bg-neo-yellow transition-all duration-500"
                                    style={{ width: `${activeGen.progress}%` }}
                                />
                            </div>
                            <p className="mt-2 text-sm font-bold uppercase">Current stage: <span className="text-neo-pink">{activeGen.current_agent || 'Waiting'}</span></p>
                        </div>
                    )}
                </section>

                <section className="flex flex-col gap-8">
                    <div className="neo-card bg-neo-black text-neo-white font-mono h-80 flex flex-col">
                        <div className="flex justify-between items-center border-b border-gray-700 pb-2 mb-4">
                            <span className="text-xs uppercase tracking-widest text-neo-yellow">Agent Swarm Terminal</span>
                            <div className="flex gap-2">
                                <div className="w-3 h-3 bg-red-500 rounded-full border border-white/20" />
                                <div className="w-3 h-3 bg-yellow-500 rounded-full border border-white/20" />
                                <div className="w-3 h-3 bg-green-500 rounded-full border border-white/20" />
                            </div>
                        </div>
                        <div className="text-sm opacity-90 overflow-y-auto flex-1 custom-scrollbar">
                            {logs.map((log, i) => (
                                <p key={i} className={log.includes('ERROR') ? 'text-red-400' : log.includes('STARTED') ? 'text-neo-cyan' : ''}>
                                    {log}
                                </p>
                            ))}
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="neo-card bg-neo-yellow">
                            <h3 className="text-lg font-black uppercase">Infrastructure</h3>
                            <p className="text-sm font-mono mt-1 opacity-80">NODES:_ACTIVE</p>
                            <p className="text-sm font-mono opacity-80">SYNC:_DUAL_OK</p>
                        </div>
                        <div className="neo-card bg-neo-cyan">
                            <h3 className="text-lg font-black uppercase">Service Mesh</h3>
                            <p className="text-sm font-mono mt-1 opacity-80">LATENCY:_18MS</p>
                            <p className="text-sm font-mono opacity-80">LOAD:_STABLE</p>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
};

export default App;
